"""CLI interface for ptx."""

import sys
import click
from . import openrouter


@click.group()
def main():
    """ptx - Experimental tool to wrap Python packages for Nix."""
    pass


@main.command()
@click.option("--prompt", "-p", type=click.Path(exists=True), help="Prompt literal text")
@click.option("--prompt-file", "-p", type=click.Path(exists=True), help="Prompt file path")
@click.option("--model", "-m", default="anthropic/claude-3.5-sonnet", help="Model to use")
def run(prompt: str, model: str):
    """Run a one-shot completion and return JSON output.

    Reads prompt from file (--prompt) or stdin if not specified.
    """
    # Read prompt from file or stdin
    if prompt:
        with open(prompt, 'r') as f:
            prompt_text = f.read()
    else:
        prompt_text = sys.stdin.read()

    if not prompt_text.strip():
        click.echo("Error: No prompt provided", err=True)
        sys.exit(1)

    try:
        response_content = openrouter.complete_chat(user_prompt=prompt_text, model=model)
        click.echo(response_content)
    except openrouter.OpenRouterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def models():
    """List available models from OpenRouter."""
    try:
        model_list = openrouter.list_models()
        click.echo("Available models:")
        for model in model_list:
            click.echo(f"  - {model['id']}")
    except openrouter.OpenRouterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
