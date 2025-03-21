"""
LeetCode Project Generator
A program that automatically generates a C project template given the LeetCode problem URL.

Author: Konrad Guzek
"""

import subprocess

import click

from .interfaces.web import get_leetcode_template, is_title_slug
from .interfaces.file import create_project, LANGUAGE_INTERFACES

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
@click.help_option("--help", "-h")
@click.argument("url_or_slug", required=False)
def lpg(
    url_or_slug: str | None = None,
    title_slug: str | None = None,
    url: str | None = None,
    lang: str = DEFAULT_PROJECT_LANGUAGE,
    directory: str = DEFAULT_PROJECT_DIRECTORY,
    force: bool = True,
    git_init: bool = False,
):
    """Creates a LeetCode skeleton project from the given problem URL or
    title slug in the specified programming language."""
    if lang not in LANGUAGE_INTERFACES:
        raise click.ClickException(f"{lang} projects are currently unsupported.")
    if url_or_slug is not None:
        if is_title_slug(url_or_slug):
            title_slug = url_or_slug
        else:
            url = url_or_slug
    title_slug, template_data = get_leetcode_template(lang, title_slug, url)
    path = create_project(title_slug, directory, template_data, force)
    if git_init:
        subprocess.run("git init", check=True)
    click.echo(f"Successfully created project at {path}!")


if __name__ == "__main__":
    lpg()
