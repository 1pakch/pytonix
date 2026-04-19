"""
PyPI package metadata types including PEP 508 dependency iteration logic.
"""

import os
import packaging
import msgspec

from pathlib import Path
from typing import Literal, Iterator

import packaging.markers
import packaging.requirements


type Pep508Environment = packaging.markers.Environment
"""Environment dict for PEP 508 dependency (marker) evaluation.

Includes marker names like "python_version", "python_full_version", "sys_platform",
"os_name", "platform_machine", "platform_system", "implementation_name", and "extra".

Use `packaging.markers.default_environment()` to get the current runtime environment.
"""


type Pep508Requirement = packaging.requirements.Requirement
"""Parsed PEP 508 dependency requirement, e.g. 'requests[security]>=2.0; python_version>="3.8"'.

Attributes: name ("requests"), extras ({"security"}), specifier (">=2.0"),
marker ('python_version >= "3.8"'), url (None unless a direct URL requirement).
"""


class PypiPackageInfo(msgspec.Struct, frozen=True):
    """Rich package information in PyPI including dependency specifications.

    Sits in the "info" attribute of a root JSON object returned for a package.
    Note some fields e.g. `description` or `description_content_type` are currently omitted.
    """

    name: str
    version: str
    summary: str | None
    requires_python: str | None
    requires_dist: list[str] | None
    provides_extra: list[str] | None
    home_page: str | None
    project_urls: dict[str, str] | None

    def iterate_requirements(
        self,
        env: Pep508Environment,
        include_extras: set[str] | Literal["none", "all"] = "none",
    ) -> Iterator[Pep508Requirement]:
        """Yield resolved requirements for this package.

        Args:
            env: Target platform environment for marker evaluation. Must be explicitly
                 provided — use `packaging.markers.default_environment()` for the current
                 runtime, or construct a custom one for the targeted environment.
            include_extras: Optional dependency groups to include (see `provides_extra`)
                - "none": unconditional deps only (default)
                - "all": unconditional deps + all declared extras
                - set[str]: unconditional deps + the specified extras

        Yields:
            Pep508Requirement for each matching dependency.
        """
        if not self.requires_dist:
            return
        resolved_extras = self._resolve_extras(include_extras)
        for s in self.requires_dist:
            r = packaging.requirements.Requirement(s)
            if self._requirement_matches(r, resolved_extras, env):
                yield r

    def _resolve_extras(
        self, include_extras: set[str] | Literal["none", "all"]
    ) -> set[str]:
        """Resolve the include_extras argument to a concrete set of extra names."""
        if include_extras == "none":
            return set()
        elif include_extras == "all":
            return set(self.provides_extra or [])
        elif isinstance(include_extras, set):
            return include_extras
        else:
            raise ValueError(
                f"include_extras must be 'all', 'none', or a set of strings, got {include_extras!r}"
            )

    def _requirement_matches(
        self, r: Pep508Requirement, resolved_extras: set[str], env: Pep508Environment
    ) -> bool:
        """Return True if the requirement should be included given the resolved extras and target environment.
        Unconditional requirements (no marker) always match.
        Conditional requirements match if any of the resolved extras satisfies the marker.
        """
        if r.marker is None:
            return True
        if not resolved_extras:
            return False
        return any(r.marker.evaluate({**env, "extra": e}) for e in resolved_extras)


class PypiReleaseDigests(msgspec.Struct, frozen=True):
    "Normally contains the hashes for the source tarball or wheel."

    sha256: str


class PypiReleaseFile(msgspec.Struct, frozen=True):
    "Ponts to a particular release of a package in PyPI."

    filename: str
    packagetype: str
    url: str
    digests: PypiReleaseDigests


class PypiPackageMetadata(msgspec.Struct, frozen=True):
    "The top-level structure about a package returned by PyPI."

    info: PypiPackageInfo
    urls: list[PypiReleaseFile]
