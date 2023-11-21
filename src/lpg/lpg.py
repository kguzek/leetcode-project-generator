"""
LeetCode Project Generator
A program that automatically generates a C project template given the LeetCode problem URL.

Author: Konrad Guzek
"""

import subprocess

import click

from interfaces import web as web_interface
from interfaces import file as file_interface

# TODO: Update
SUPPORTED_LANGUAGES = ["c"]


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
    default="c",
)
@click.option(
    "--directory",
    "-d",
    help="The directory for the project to be created in.",
    default=R"~/Documents/Coding/{language_name}/leetcode/",
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
    title_slug: str, url: str, lang: str, directory: str, force: bool, git_init: bool
):
    """CLI Entry point."""
    if lang not in SUPPORTED_LANGUAGES:
        raise click.ClickException(f"Unsupported language {lang}.")
    title_slug, template_data = web_interface.get_leetcode_template(
        title_slug, url, lang
    )
    title_slug = "least-sum"
    file_interface.create_project(title_slug, directory, template_data, force)
    if git_init:
        subprocess.run("git init")


if __name__ == "__main__":
    lpg()
