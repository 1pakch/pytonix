"""Read and write NixFlake objects to/from directories."""

from pathlib import Path

from ..domain.packaging import NixFlake


def write_flake(flake: NixFlake, directory: str | Path) -> list[Path]:
    """Write NixFlake to directory, creating subdirectories as needed.

    Raises:
        ValueError: If flake contains invalid paths.
    """
    dest_path = Path(directory)
    dest_path.mkdir(parents=True, exist_ok=True)

    written_files = []

    for rel_path, contents in flake.files.items():
        file_path = dest_path / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as f:
            f.write(contents)

        written_files.append(file_path)

    return written_files


def read_flake(directory: str | Path) -> NixFlake:
    """Read NixFlake from directory. Requires flake.nix, ignores flake.lock.

    Raises:
        FileNotFoundError: If directory doesn't exist.
        NotADirectoryError: If path is not a directory.
        ValueError: If flake.nix is not found or paths are invalid.
    """
    src_path = Path(directory)

    if not src_path.exists():
        raise FileNotFoundError(f"Directory not found: {src_path}")

    if not src_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {src_path}")

    # Validate flake.nix exists
    flake_nix = src_path / "flake.nix"
    if not flake_nix.exists():
        raise ValueError(f"flake.nix not found in {src_path}")

    files = {}

    # Recursively read all files except flake.lock
    for file_path in src_path.rglob("*"):
        if file_path.is_file() and file_path.name != "flake.lock":
            rel_path = str(file_path.relative_to(src_path))
            with open(file_path, "r") as f:
                files[rel_path] = f.read()

    return NixFlake(files=files)
