"""CLI interface for ptx."""

import sys
import click
import packaging.markers

from pytonix.infra import openrouter, pypi
from pytonix.infra.openrouter import DEFAULT_MODEL


@click.group()
def main():
    """ptx - Experimental harness for nixifying Python packages."""
    pass


@main.group("llm")
def llm_group():
    """LLM-related commands."""
    pass


@main.group("pypi")
def pypi_group():
    """PyPI package commands."""
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


@pypi_group.command("show-deps")
@click.argument("package")
@click.option("--version", "-v", default=None, help="Package version (default: latest)")
@click.option("--max-depth", "-d", default=None, type=int, help="Maximum recursion depth")
def deps_cli_cmd(package: str, version: str | None, max_depth: int | None):
    """Print dependency tree for a PyPI package (depth-first traversal).

    Traverses the dependency graph depth-first. Packages appearing multiple
    times are marked (seen) and not traversed again.
    """
    env = packaging.markers.default_environment()
    visited = set()

    def print_package(name: str, depth: int, annotation: str = ""):
        indent = "  "
        suffix = f" {annotation}" if annotation else ""
        print(indent * depth + name + suffix)

    def handle_fetch_error(name: str, error: Exception):
        import httpx
        if isinstance(error, httpx.HTTPStatusError):
            if error.response.status_code == 404:
                click.echo(f"Error: Package '{name}' not found on PyPI", err=True)
            else:
                click.echo(f"Error: HTTP {error.response.status_code} when fetching '{name}'", err=True)
        else:
            click.echo(f"Error: {error}", err=True)
        sys.exit(1)

    def fetch_package(name: str, depth: int):
        pkg_version = version if depth == 0 else None
        return pypi.get_pypi_metadata(name, pkg_version)

    def traverse(name: str, depth: int = 0):
        if name in visited:
            print_package(name, depth, "(seen)")
            return

        if max_depth is not None and depth >= max_depth:
            print_package(name, depth, "(max depth reached)")
            return

        try:
            pkg = fetch_package(name, depth)
            visited.add(name)
            print_package(name, depth)

            for req in pkg.info.iterate_requirements(env, include_extras="none"):
                traverse(req.name, depth + 1)
        except Exception as e:
            if depth == 0:
                handle_fetch_error(name, e)

    traverse(package)


if __name__ == "__main__":
    main()
