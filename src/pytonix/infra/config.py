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
