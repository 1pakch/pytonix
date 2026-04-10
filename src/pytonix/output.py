import msgspec
from pathlib import Path

type RelativePath = str
type FileContents = str
type SerializedFiles = dict[RelativePath, FileContents]


class CodegenResponse(msgspec.Struct):
    files: SerializedFiles
    comments: list[str]

    def __post_init__(self):
        validate_paths(self.files)


def validate_paths(files: SerializedFiles) -> None:
    """Validate that all file paths are relative (not absolute).

    Raises:
        ValueError: If any path is absolute.
    """
    for rel_path in files:
        if Path(rel_path).is_absolute():
            raise ValueError(f"Absolute paths not allowed: {rel_path}")


def parse_codegen_response(json_input: str) -> CodegenResponse:
    """Parse JSON string into CodegenResponse.

    Args:
        json_input: JSON string to parse.

    Returns:
        Parsed CodegenResponse object.

    Raises:
        msgspec.DecodeError: If JSON is malformed.
        ValueError: If validation fails (e.g., absolute paths).
    """
    return msgspec.json.decode(json_input, type=CodegenResponse)


def extract_files(response: CodegenResponse, directory: str | Path) -> list[Path]:
    """Extract files from response and write to directory.

    Returns list of files written (including comments file if present).
    """
    dest_path = Path(directory)
    dest_path.mkdir(parents=True, exist_ok=True)

    written_files = []

    for rel_path, contents in response.files.items():
        file_path = dest_path / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as f:
            f.write(contents)

        written_files.append(file_path)

    if response.comments:
        comments_file = dest_path / "comments"
        with open(comments_file, 'w') as f:
            for comment in response.comments:
                f.write(f"{comment}\n")
        written_files.append(comments_file)

    return written_files
