"""
LeetCode Project Generator
A program that automatically generates a C project template given the LeetCode problem URL.

Author: Konrad Guzek
"""

import subprocess

import click

from .interfaces import web as web_interface
from .interfaces import file as file_interface

SUPPORTED_LANGUAGES = ["c"]

DEFAULT_PROJECT_LANGUAGE = "c"
DEFAULT_PROJECT_DIRECTORY = R"~/Documents/Coding/{language_name}/leetcode/"


@click.command()
@click.option(
    "--title-slug",
    "-s",
    help="The dash-separated name of the problem as it appears in the URL.",
)
@click.option(
    "--url",
    "-u",
    help="The URL to the LeetCode problem webpage.",
)
@click.option(
    "--lang",
    "-l",
    help="The language of the code to generate.",
    default=DEFAULT_PROJECT_LANGUAGE,
)
@click.option(
    "--directory",
    "-d",
    help="The directory for the project to be created in.",
    default=DEFAULT_PROJECT_DIRECTORY,
)
@click.option(
    "--force",
    "-f",
    help="Force-creates the project directory even if it already exists.",
    default=False,
    is_flag=True,
    show_default=True,
)
@click.option(
    "--git-init",
    "-g",
    help="Initialises a git repository in the project directory.",
    default=False,
    is_flag=True,
    show_default=False,
)
def lpg(
    title_slug: str | None = None,
    url: str | None = None,
    lang: str = DEFAULT_PROJECT_LANGUAGE,
    directory: str = DEFAULT_PROJECT_DIRECTORY,
    force: bool = True,
    git_init: bool = False,
):
    """CLI Entry point."""
    if lang not in SUPPORTED_LANGUAGES:
        raise click.ClickException(f"{lang} projects are currently unsupported.")
    title_slug, template_data = web_interface.get_leetcode_template(
        lang, title_slug, url
    )
    path = file_interface.create_project(title_slug, directory, template_data, force)
    if git_init:
        subprocess.run("git init", check=True)
    click.echo(f"Successfully created project at {path}!")


if __name__ == "__main__":
    lpg()
