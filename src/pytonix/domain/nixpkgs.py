import msgspec

from datetime import datetime
from pathlib import Path
from typing import Self


type NixpkgsRefStr = str
"A flake ref string possibly to a moving target e.g. 'github:NixOS/nixpkgs/nixos-unstable'."


type ResolvedNixpkgsRef = str
"A flake ref string pointing to a specific revision e.g 'github:NixOS/nixpkgs/4bd9165a91'."


class JsonStrMixin:
    @classmethod
    def from_json_str(cls, data: str) -> Self:
        return msgspec.json.decode(data.encode(), type=cls)

    def to_json_str(self) -> str:
        return msgspec.json.encode(self).decode()


class NixpkgsRef(msgspec.Struct, frozen=True):
    """A flake ref as a parsed structure.

    Note: Uses camelCase field names to mirror nix JSON output exactly.
    """

    owner: str
    repo: str
    type: str
    ref: str | None = None
    rev: str | None = None
    lastModified: int | None = None

    def __str__(self) -> NixpkgsRefStr:
        pin = self.rev or self.ref
        return f"{self.type}:{self.owner}/{self.repo}/{pin}"


class PrefetchedNixpkgsRef(JsonStrMixin, msgspec.Struct, frozen=True):
    """The structure returned by `nix flake prefetch`.

    Note: Uses camelCase field names to mirror nix JSON output exactly.
    """

    hash: str
    storePath: str
    locked: NixpkgsRef
    original: NixpkgsRef

    def to_str(self) -> NixpkgsRefStr:
        return str(self.locked)
