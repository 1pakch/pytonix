"""Manual tests for PyPI fetching (requires network)."""

import packaging.markers
from pytonix.infra.pypi import get_pypi_metadata, get_sdist_release


def test_fetch_ott_jax():
    """Fetch ott-jax 0.6.0 and verify basic metadata."""
    pkg = get_pypi_metadata("ott-jax", "0.6.0")

    assert pkg.info.name == "ott-jax"
    assert pkg.info.version == "0.6.0"
    assert pkg.info.requires_python == ">=3.9"
    assert pkg.info.provides_extra == ["neural", "dev", "test", "docs"]

    # Check sdist
    sdist = get_sdist_release(pkg)
    assert sdist is not None
    assert sdist.packagetype == "sdist"
    assert "ott_jax-0.6.0.tar.gz" in sdist.url


def test_iterate_requirements_ott_jax():
    """Test requirement iteration on real package."""
    pkg = get_pypi_metadata("ott-jax", "0.6.0")
    env = packaging.markers.default_environment()

    # No extras
    reqs_none = list(pkg.info.iterate_requirements(env, include_extras="none"))
    assert len(reqs_none) == 5
    assert {r.name for r in reqs_none} == {"jax", "jaxopt", "lineax", "numpy", "optax"}

    # All extras
    reqs_all = list(pkg.info.iterate_requirements(env, include_extras="all"))
    assert len(reqs_all) > 20  # Should have many deps with all extras

    # Neural extra only
    reqs_neural = list(pkg.info.iterate_requirements(env, include_extras={"neural"}))
    assert len(reqs_neural) == 8
    assert "flax" in {r.name for r in reqs_neural}
