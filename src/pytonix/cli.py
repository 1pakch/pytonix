"""CLI interface for ptx."""

import sys
import click

from pytonix.infra import openrouter
from pytonix.infra.openrouter import DEFAULT_MODEL


@click.group()
def main():
    """ptx - Experimental harness for nixifying Python packages."""
    pass


@main.group("llm")
def llm_group():
    """LLM-related commands."""
    pass


@llm_group.command("one-shot")
@click.option("--model", "-m", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
def one_shot_cli_cmd(model: str):
    """Run a one-shot completion.

    Reads the (user) prompt from stdin.
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


@llm_group.command("list-models")
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
