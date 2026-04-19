"""Execute Nix commands with logging."""

import subprocess
from pathlib import Path

import msgspec


class BuildResult(msgspec.Struct, frozen=True):
    """Result of a nix build command execution."""

    exit_code: int
    stdout_path: Path
    stderr_path: Path

    def success(self) -> bool:
        return 0 == exit_code


def execute_command(
    cmd: list[str],
    cwd: Path,
    stdout_path: Path,
    stderr_path: Path,
) -> int:
    """Execute command with output streaming to log files.

    Returns:
        Exit code of the process
    """
    with open(stdout_path, "w") as stdout_file, open(stderr_path, "w") as stderr_file:
        process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
        )
        return process.wait()


def prepare_log_directory(log_dir: str | Path, target_name: str) -> tuple[Path, Path]:
    """Create log directory and return paths for stdout/stderr.

    Returns:
        Tuple of (stdout_path, stderr_path)
    """
    target_log_dir = Path(log_dir) / target_name
    target_log_dir.mkdir(parents=True, exist_ok=True)

    stdout_path = target_log_dir / "stdout"
    stderr_path = target_log_dir / "stderr"

    return stdout_path, stderr_path


def build_nix_command(flake_ref: str, extra_args: list[str] | None = None) -> list[str]:
    """Build the nix command argument list.

    Args:
        flake_ref: Flake reference (e.g., ".", ".#default", ".#packages.x86_64-linux.mypackage")
        extra_args: Additional arguments to pass to nix build
    """
    cmd = ["nix", "build", flake_ref, "--no-link"]
    if extra_args:
        cmd.extend(extra_args)
    return cmd


def run_nix_build(
    flake_dir: str | Path,
    flake_ref: str = ".",
    target_name: str = "default",
    log_dir: str | Path = "logs/build",
    extra_args: list[str] | None = None,
) -> BuildResult:
    """Run nix build command capturing stdout and stderr.

    Args:
        flake_dir: Directory containing flake.nix
        flake_ref: Flake reference to build (e.g., ".", ".#default", ".#mypackage")
        target_name: Name for the log subdirectory (e.g., "default", "mypackage")
        log_dir: Base directory for logs (default: logs/build)
        extra_args: Additional arguments to pass to nix build

    Returns:
        BuildResult with exit code, log paths, and success status

    Raises:
        FileNotFoundError: If flake_dir doesn't exist or no flake.nix found.
    """
    stdout_path, stderr_path = prepare_log_directory(log_dir, target_name)
    cmd = build_nix_command(flake_ref, extra_args)
    exit_code = execute_command(cmd, flake_path, stdout_path, stderr_path)

    return BuildResult(
        exit_code=exit_code,
        stdout_path=stdout_path,
        stderr_path=stderr_path,
        success=exit_code == 0,
    )
