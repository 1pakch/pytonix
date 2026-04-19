import gzip
import ijson
import json
import re
import shutil
import subprocess

from functools import cache
from pathlib import Path

from pytonix.domain.nixpkgs import NixpkgsRefStr, PrefetchedNixpkgsRef
from pytonix.infra.config import get_packages_info_cache_dir


# Regex to match python package keys like "python313Packages.requests"
PYTHON_PACKAGE_RE = re.compile(r'^python(\d+)Packages\.(.+)$')


@cache
def nix_version_to_dotted(nix_ver: str) -> str:
    """Convert nix version '313' to '3.13', '39' to '3.9'"""
    if len(nix_ver) == 2:  # "39" -> "3.9"
        return f"3.{nix_ver[1]}"
    return f"3.{nix_ver[1:]}"  # "313" -> "3.13"


@cache
def dotted_version_to_nix(dotted_ver: str) -> str:
    """Convert dotted version '3.13' to '313', '3.9' to '39'"""
    return dotted_ver.replace(".", "")


# Nix expression to evaluate packages-info.nix from a nixpkgs flake.
# This generates structured package metadata used by nixpkgs package indexes/caches
# like https://search.nixos.org.
# The output is a JSON structure containing all package metadata (name, version, description, etc.)
_PACKAGES_INFO_TEMPLATE = """
let
  nixpkgs = builtins.getFlake "$nixpkgs-ref";
in
  import (nixpkgs + "/pkgs/top-level/packages-info.nix") {}
"""


def prefetch_flake(ref: NixpkgsRefStr) -> PrefetchedNixpkgsRef:
    """Prefetch a flake and return the resolved reference with hash and store path."""
    result = subprocess.run(
        ["nix", "flake", "prefetch", "--json", ref],
        capture_output=True,
        text=True,
        check=True,
    )
    return PrefetchedNixpkgsRef.from_json_str(result.stdout)


def get_packages_info(ref: PrefetchedNixpkgsRef | NixpkgsRefStr) -> Path:
    """
    Generate packages-info.json.gz for a nixpkgs flake ref.

    This evaluates nixpkgs' packages-info.nix to get the complete package metadata
    used by package indexing services like https://search.nixos.org.

    Returns the path to the cached packages-info.json.gz file.
    If already cached, returns the existing file without regenerating.
    """
    # Prefetch if we got a string ref
    if isinstance(ref, str):
        prefetched = prefetch_flake(ref)
    else:
        prefetched = ref

    # Build cache path: packages-info/{owner}/{repo}/{rev}/packages-info.json.gz
    owner = prefetched.locked.owner
    repo = prefetched.locked.repo
    rev = prefetched.locked.rev
    cache_dir = get_packages_info_cache_dir(owner, repo, rev)
    cache_file = cache_dir / "packages-info.json.gz"

    # Return cached file if it exists
    if cache_file.exists():
        return cache_file

    # Generate the nix expression by substituting the flake ref
    flake_ref = str(prefetched.locked)
    nix_expr = _PACKAGES_INFO_TEMPLATE.replace("$nixpkgs-ref", flake_ref)

    # Call nix-instantiate with --raw to get the JSON string without double-encoding
    # packages-info.nix uses builtins.toJSON internally, so --raw gives us the JSON directly
    proc = subprocess.Popen(
        ["nix-instantiate", "--eval", "--raw", "--expr", nix_expr],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    with gzip.open(cache_file, "wb") as f:
        shutil.copyfileobj(proc.stdout, f)

    proc.wait()
    if proc.returncode != 0:
        stderr = proc.stderr.read().decode()
        raise subprocess.CalledProcessError(proc.returncode, proc.args, stderr=stderr)

    return cache_file


def get_and_index_nixpkgs(ref: NixpkgsRefStr | PrefetchedNixpkgsRef) -> tuple[PrefetchedNixpkgsRef, Path]:
    """
    Get and index nixpkgs packages.

    Steps:
    1. Prefetch the flake ref
    2. Generate packages-info.json.gz
    3. Index Python packages into separate files

    Returns:
        (prefetched_ref, cache_dir)
    """
    # Prefetch
    if isinstance(ref, str):
        prefetched = prefetch_flake(ref)
    else:
        prefetched = ref

    # Get cache directory
    owner = prefetched.locked.owner
    repo = prefetched.locked.repo
    rev = prefetched.locked.rev
    cache_dir = get_packages_info_cache_dir(owner, repo, rev)

    # Ensure packages-info.json.gz exists
    packages_info_path = get_packages_info(prefetched)

    # Check if indexing already done
    marker_file = cache_dir / ".python-packages-indexed"
    if not marker_file.exists():
        _parse_python_packages(packages_info_path, cache_dir)
        marker_file.touch()

    return prefetched, cache_dir


def _parse_python_packages(packages_info_path: Path, cache_dir: Path):
    """
    Parse packages-info.json.gz and extract Python package names by version.
    Writes separate files for each Python version (e.g., python313.txt, python39.txt).
    """
    version_files = {}

    try:
        with gzip.open(packages_info_path, "rb") as f:
            parser = ijson.kvitems(f, "packages")

            for key, value in parser:
                match = PYTHON_PACKAGE_RE.match(key)
                if match:
                    version = match.group(1)  # "313"
                    package_name = match.group(2)  # "requests"

                    if version not in version_files:
                        file_path = cache_dir / f"python{version}.txt"
                        version_files[version] = open(file_path, "w")

                    version_files[version].write(package_name + "\n")
    finally:
        for f in version_files.values():
            f.close()


def get_python_packages_index(
    ref: PrefetchedNixpkgsRef | NixpkgsRefStr,
    python_version: str | None = None,
) -> dict[str, set[str]] | set[str]:
    """
    Get index of Python packages for a nixpkgs revision.

    Args:
        ref: Nixpkgs flake reference
        python_version: Nix version like "313", "39", "311" (optional)

    Returns:
        If python_version is None: dict mapping all versions to package name sets
        If python_version specified: set of package names for that version
    """
    # Get and index nixpkgs
    prefetched, cache_dir = get_and_index_nixpkgs(ref)

    # If specific version requested, read that file
    if python_version is not None:
        version_file = cache_dir / f"python{python_version}.txt"
        if not version_file.exists():
            return set()
        with open(version_file) as f:
            return {line.strip() for line in f if line.strip()}

    # Otherwise build full index from all files
    index = {}
    for file_path in cache_dir.glob("python*.txt"):
        version = file_path.stem.replace("python", "")
        with open(file_path) as f:
            index[version] = {line.strip() for line in f if line.strip()}

    return index


def lookup_python_package(
    ref: PrefetchedNixpkgsRef | NixpkgsRefStr,
    python_version: str,
    pname: str,
) -> bool:
    """
    Check if a Python package exists in nixpkgs for a specific Python version.

    Args:
        ref: Nixpkgs flake reference
        python_version: Python version like "39", "310", "311"
        pname: Package name to look up

    Returns:
        True if package exists, False otherwise
    """
    packages = get_python_packages_index(ref, python_version)
    return pname in packages


# TODO: add functionality to add, remove and view roots associated to nxipkg rvisions
