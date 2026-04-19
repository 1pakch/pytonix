import gzip
import shutil
import subprocess

from pathlib import Path

from pytonix.domain.nixpkgs import NixpkgsRefStr, PrefetchedNixpkgsRef
from pytonix.infra.config import get_packages_info_cache_dir


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
    cache_file = get_packages_info_cache_dir(owner, repo, rev, "packages-info.json.gz")

    # Return cached file if it exists
    if cache_file.exists():
        return cache_file

    # Generate the nix expression by substituting the flake ref
    flake_ref = str(prefetched.locked)
    nix_expr = _PACKAGES_INFO_TEMPLATE.replace("$nixpkgs-ref", flake_ref)

    # Call nix-instantiate and pipe output directly to gzip
    proc = subprocess.Popen(
        ["nix-instantiate", "--eval", "--json", "--expr", nix_expr],
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


# TODO: add functionality to add, remove and view roots associated to nxipkg rvisions
