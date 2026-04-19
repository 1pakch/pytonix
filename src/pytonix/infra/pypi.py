"""
PyPI JSON API client with filesystem caching.

Always reads from cache if present, otherwise fetches and writes to cache.
"""

import os
import httpx
import msgspec
from pathlib import Path

from pytonix.domain.pypi import PypiPackageMetadata, PypiReleaseFile
from .config import get_pypi_cache_dir


PYPI_BASE = "https://pypi.org/pypi"


def _get_metadata_cache_path(package: str, version: str | None) -> Path:
    fname = f"{package}@{version}.json" if version else f"{package}.json"
    return get_pypi_cache_dir("json") / fname


def _fetch_pypi_metadata(package: str, version: str | None) -> bytes:
    resource = package if not version else f"{package}/{version}"
    url = f"{PYPI_BASE}/{resource}/json"
    response = httpx.get(url, follow_redirects=True)
    response.raise_for_status()
    return response.content


def get_pypi_metadata(package: str, version: str | None = None) -> PypiPackageMetadata:
    """Retrieve PyPI metadata for a package, using cache if available."""
    path = _get_metadata_cache_path(package, version)
    if path.exists():
        raw = path.read_bytes()
    else:
        raw = _fetch_pypi_metadata(package, version)
        path.write_bytes(raw)
    return msgspec.json.decode(raw, type=PypiPackageMetadata)


def get_sdist_release(pkg: PypiPackageMetadata) -> PypiReleaseFile | None:
    """Return the source distribution file, if present."""
    for f in pkg.urls:
        if f.packagetype == "sdist":
            return f
    return None


# --- Quick smoke test ---

if __name__ == "__main__":
    import sys

    name = sys.argv[1] if len(sys.argv) > 1 else "ott-jax"
    version = "0.6.0"
    pkg = get_pypi_metadata(name, "0.6.0")
    src = get_sdist_release(pkg)

    print(f"name:           {pkg.info.name}")
    print(f"version:        {pkg.info.version}")
    print(f"provides_extra: {pkg.info.provides_extra}")
    print(f"requires_python:{pkg.info.requires_python}")
    print(f"sdist url:      {src.url if src else 'n/a'}")
    print(f"sdist sha256:   {src.digests.sha256 if src else 'n/a'}")
    print(f"deps ({len(pkg.info.requires_dist or [])}):")
    for dep in pkg.info.requires_dist or []:
        print(f"  {dep}")

    import packaging.markers

    env = packaging.markers.default_environment()
    print([r.name for r in pkg.info.iterate_requirements(env)])
    print([r.name for r in pkg.info.iterate_requirements(env, include_extras="none")])
    print([r.name for r in pkg.info.iterate_requirements(env, include_extras="all")])
    print(
        [r.name for r in pkg.info.iterate_requirements(env, include_extras={"neural"})]
    )
