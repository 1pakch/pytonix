"""CLI interface for ptx."""

import os
import sys
import json
import click
import httpx


@click.group()
def main():
    """ptx - Experimental tool to wrap Python packages for Nix."""
    pass


@main.command()
@click.option("--prompt", "-p", type=click.Path(exists=True), help="Prompt file path")
@click.option("--model", "-m", default="anthropic/claude-3.5-sonnet", help="Model to use")
def run(prompt: str, model: str):
    """Run a one-shot completion and return JSON output.

    Reads prompt from file (--prompt) or stdin if not specified.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        click.echo("Error: OPENROUTER_API_KEY environment variable not set", err=True)
        sys.exit(1)

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
        with httpx.Client() as client:
            response = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt_text}],
                },
                timeout=60.0
            )
            response.raise_for_status()
            data = response.json()

            # Output the response content
            click.echo(data["choices"][0]["message"]["content"])

    except httpx.HTTPError as e:
        click.echo(f"HTTP Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
def models():
    """List available models from OpenRouter."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        click.echo("Error: OPENROUTER_API_KEY environment variable not set", err=True)
        sys.exit(1)

    try:
        with httpx.Client() as client:
            response = client.get(
                "https://openrouter.ai/api/v1/models",
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()

            click.echo("Available models:")
            for model in data.get("data", []):
                click.echo(f"  - {model['id']}")

    except httpx.HTTPError as e:
        click.echo(f"HTTP Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
