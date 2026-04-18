"""
PyPI JSON API client with filesystem caching.

Cache location: $PYPI_CACHE_DIR (required env var)
Always reads from cache if present, otherwise fetches and writes to cache.
"""

import os
from pathlib import Path

import httpx
import msgspec


PYPI_BASE = "https://pypi.org/pypi"


# --- Data model (partial; extend as needed) ---

class Digests(msgspec.Struct):
    sha256: str


class ReleaseFile(msgspec.Struct):
    filename: str
    packagetype: str
    url: str
    digests: Digests


class PackageInfo(msgspec.Struct):
    name: str
    version: str
    summary: str | None
    requires_python: str | None
    requires_dist: list[str] | None
    home_page: str | None
    project_urls: dict[str, str] | None


class PyPIPackage(msgspec.Struct):
    info: PackageInfo
    urls: list[ReleaseFile]


# --- Cache helpers ---

def _cache_dir() -> Path:
    raw = os.environ.get("PYPI_CACHE_DIR")
    if not raw:
        raise EnvironmentError("PYPI_CACHE_DIR is not set")
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _cache_path(package: str, version: str | None) -> Path:
    name = f"{package}@{version}.json" if version else f"{package}.json"
    return _cache_dir() / name


# --- Fetch ---

def _fetch_raw(package: str, version: str | None) -> bytes:
    url = f"{PYPI_BASE}/{package}/json" if version is None else f"{PYPI_BASE}/{package}/{version}/json"
    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()
    return response.content


def _parse(raw: bytes) -> PyPIPackage:
    return msgspec.json.decode(raw, type=PyPIPackage)


# --- Public API ---

def query_pypi(package: str, version: str | None = None) -> PyPIPackage:
    """Fetch PyPI metadata for a package, using cache if available."""
    path = _cache_path(package, version)
    if path.exists():
        return _parse(path.read_bytes())
    raw = _fetch_raw(package, version)
    path.write_bytes(raw)
    return _parse(raw)


# --- Convenience extractors ---

def get_sdist_release(pkg: PyPIPackage) -> ReleaseFile | None:
    """Return the source distribution file, if present."""
    for f in pkg.urls:
        if f.packagetype == "sdist":
            return f
    return None


# --- Quick smoke test ---

if __name__ == "__main__":
    import sys

    name = sys.argv[1] if len(sys.argv) > 1 else "ott-jax"
    pkg = query_pypi(name)
    src = get_sdist_release(pkg)

    print(f"name:           {pkg.info.name}")
    print(f"version:        {pkg.info.version}")
    print(f"requires_python:{pkg.info.requires_python}")
    print(f"sdist url:      {src.url if src else 'n/a'}")
    print(f"sdist sha256:   {src.digests.sha256 if src else 'n/a'}")
    print(f"deps ({len(pkg.info.requires_dist or [])}):")
    for dep in pkg.info.requires_dist or []:
        print(f"  {dep}")
