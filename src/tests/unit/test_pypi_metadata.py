"""Minimal unit tests for PyPI metadata parsing (no network calls)."""

import packaging.markers
from pytonix.domain.pypi import PypiPackageInfo


def test_iterate_requirements_basic():
    """Test basic requirement iteration with extras."""
    pkg = PypiPackageInfo(
        name="pkg",
        version="1.0",
        summary=None,
        requires_python=None,
        requires_dist=["requests", 'pytest; extra == "dev"'],
        provides_extra=["dev"],
        home_page=None,
        project_urls=None,
    )
    env = packaging.markers.default_environment()

    # No extras
    assert [r.name for r in pkg.iterate_requirements(env, "none")] == ["requests"]

    # With extras
    assert {r.name for r in pkg.iterate_requirements(env, "all")} == {
        "requests",
        "pytest",
    }
