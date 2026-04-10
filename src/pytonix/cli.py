"""CLI interface for ptx."""

import sys
import click

from pathlib import Path

from . import openrouter
from . import output 

from .openrouter import DEFAULT_MODEL


@click.group()
def main():
    """ptx - Experimental tool to wrap Python packages for Nix."""
    pass


@main.command("one-shot")
@click.option("--model", "-m", default=DEFAULT_MODEL, help= f"Model to use (default: {DEFAULT_MODEL})")
def one_shot_cli_cmd(model: str):
    """Run a one-shot completion and return JSON output.

    Reads the (user) prompt from the stdin.
    """
    prompt_text = sys.stdin.read()

    if not prompt_text.strip():
        click.echo("Error: No prompt provided", err=True)
        sys.exit(1)

    try:
        response_content = openrouter.complete_chat(user_prompt=prompt_text, model=model)
        click.echo(response_content)
    except openrouter.OpenRouterError as e:
        click.echo(str(e), err=True)
        sys.exit(1)


@main.command("extract-files")
@click.argument("directory", default=".")
def extract_files_cli_cmd(directory: str):
    """Extract files from the JSON output and write them to the disk.

    Reads JSON from the stdin.
    """
    json_input = sys.stdin.read()

    if not json_input.strip():
        click.echo("Error: No JSON input provided", err=True)
        sys.exit(1)

    try:
        codegen = output.parse_codegen_response(json_input)
    except Exception as e:
        click.echo(f"Error: Failed to parse JSON: {e}", err=True)
        sys.exit(1)

    try:
        written_files = output.extract_files(codegen, directory)
        for file_path in written_files:
            click.echo(f"Wrote: {file_path}", err=True)
    except OSError as e:
        click.echo(f"OS Error: {e}", err=True)
        sys.exit(1)


@main.command("list-models")
def list_models_cli_cmd():
    """List available models from OpenRouter."""
    try:
        model_list = openrouter.list_models()
        click.echo("Available models:")
        for model in model_list:
            click.echo(f"  - {model['id']}")
    except openrouter.OpenRouterError as e:
        click.echo(str(e), err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
