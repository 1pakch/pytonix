import os
import platformdirs

from pathlib import Path


def get_pypi_cache_dir(*extra_parts: str) -> Path:
    envvar = os.environ.get("PYPI_CACHE_DIR")
    if envvar:
        root = Path(envvar)
    else:
        root = platformdirs.user_cache_path(appname="pytonix") / "pypi"
    path = root.joinpath(*extra_parts) if extra_parts else root
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_packages_info_cache_dir(*extra_parts: str) -> Path:
    """Get cache directory for packages-info.json and derived caches like pythonPackages3xx."""
    envvar = os.environ.get("PACKAGES_INFO_CACHE_DIR")
    if envvar:
        root = Path(envvar)
    else:
        root = platformdirs.user_cache_path(appname="pytonix") / "packages-info"
    path = root.joinpath(*extra_parts) if extra_parts else root
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_default_nixpkgs_ref() -> str:
    """Get default nixpkgs reference from environment or fallback."""
    return os.environ.get("PTX_DEFAULT_NIXPKGS_REF", "github:NixOS/nixpkgs/nixos-unstable")
