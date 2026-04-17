from datetime import datetime
import msgspec


type RelativePath = str
type FileContents = str


class HashableStruct(msgspec.Struct):
    def hash(self) -> str:
        return hashlib.sha256(msgspec.json.encode(self)).hexdigest()


class PypiPackage(HashableStruct, frozen=True, tag=True):
    "A (versioned) Python package published in PyPI."

    name: str
    version: str


class PythonPackagingTask(HashableStruct, frozen=True, tag=True):
    "A task of nix-ifiying Python packages against a specific version of nixpkgs."

    targets: list[PypiPackage]
    nixpkgs_revision: str

    def hash(self) -> str:
        "Hash after sorting the targets."
        return hashlib.sha256(msgspec.json.encode(self._normalized())).hexdigest()

    def _normalized(self):
        "Ensures the targets are sorted for hashing."
        return PythonPackagingTask(
            targets=sorted(self.targets, key=lambda p: p.name),
            nixpkgs_revision=self.nixpkgs_revision,
        )


class NixFlake(msgspec.Struct, frozen=True, tag=True):
    "A nix flake for a packaging task."

    files: dict[RelativePath, FileContents]
