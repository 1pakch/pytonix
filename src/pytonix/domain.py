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


class Authorship(msgspec.Struct, tag=False):

    "Not supposed to be instantiated directly - use HumanAuthored of AgentAuthored."

    author_id: str
    timestamp: datetime


class HumanAuthored(Authorship, frozen=True, tag=True):

    "Metadata on human-produced packaging solutions/attempts."

    notes: str | None = None


class AgentAuthored(Authorship, frozen=True, tag=True):

    "Metadata on agent-produced packaging solutions/attempts."

    llm_model: str
    notes: str | None = None


class PackagingAttempt(msgspec.Struct, frozen=True, tag=True):

    "An attempt to solve a packaging task."

    task: PythonPackagingTask
    result: NixFlake
    authorship: HumanAuthored | AgentAuthored


