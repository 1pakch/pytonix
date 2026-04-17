"""Tests for flake read/write operations."""

import pytest
from pathlib import Path
from pytonix.domain.packaging import NixFlake
from pytonix.infra.flakes import read_flake, write_flake

# tmp_path is a pytest fixture providing a temporary directory
# that's automatically created before each test and cleaned up after


def test_write_and_read_roundtrip(tmp_path):
    """Write a flake and read it back."""
    flake = NixFlake(
        files={
            "flake.nix": "{ description = \"test\"; }",
            "default.nix": "{ }",
            "src/module.nix": "{ foo = 1; }",
        }
    )

    # Write flake
    written = write_flake(flake, tmp_path)
    assert len(written) == 3
    assert (tmp_path / "flake.nix").exists()
    assert (tmp_path / "src/module.nix").exists()

    # Read it back
    flake_read = read_flake(tmp_path)
    assert flake_read.files == flake.files


def test_read_flake_ignores_lock_file(tmp_path):
    """flake.lock should be ignored when reading."""
    (tmp_path / "flake.nix").write_text("{ }")
    (tmp_path / "flake.lock").write_text("lock content")

    flake = read_flake(tmp_path)
    assert "flake.nix" in flake.files
    assert "flake.lock" not in flake.files


def test_read_flake_requires_flake_nix(tmp_path):
    """Reading a directory without flake.nix should fail."""
    (tmp_path / "other.nix").write_text("{ }")

    with pytest.raises(ValueError, match="flake.nix not found"):
        read_flake(tmp_path)


def test_read_nonexistent_directory():
    """Reading a nonexistent directory should fail."""
    with pytest.raises(FileNotFoundError):
        read_flake("/nonexistent/path")


def test_write_creates_subdirectories(tmp_path):
    """Writing should create nested directories."""
    flake = NixFlake(
        files={
            "flake.nix": "{ }",
            "a/b/c/deep.nix": "nested",
        }
    )

    write_flake(flake, tmp_path)
    assert (tmp_path / "a/b/c/deep.nix").exists()
    assert (tmp_path / "a/b/c/deep.nix").read_text() == "nested"


def test_invalid_path_with_parent_reference():
    """Flake with '..' in path should fail validation."""
    with pytest.raises(ValueError, match="security risk"):
        NixFlake(files={"../escape.nix": "bad"})


def test_invalid_absolute_path():
    """Flake with absolute path should fail validation."""
    with pytest.raises(ValueError, match="must be relative"):
        NixFlake(files={"/absolute/path.nix": "bad"})
