"""API for accessing various OS and filesystem functions."""


import os
from click import ClickException

from .lang import c


def create_project_directory(project_path: str, force: bool):
    """Creates the project directory. If it already exists, throws a `ClickException`."""
    try:
        os.makedirs(project_path, exist_ok=force)
    except FileExistsError as error:
        raise ClickException(
            f"Cannot create project with path '{project_path}' as it already exists."
        ) from error
    except OSError as error:
        raise ClickException(f"Invalid project path '{project_path}'") from error
    return project_path


def create_project(
    project_name: str, project_directory: str, template_data: dict, force: bool
):
    """Creates the entire project."""

    language_code = template_data["langSlug"]
    language_name = template_data["lang"]
    template = template_data["code"]

    project_path = os.path.expanduser(
        os.path.join(
            project_directory.format(language_name=language_name), project_name
        )
    )
    create_project_directory(project_path, force)
    os.chdir(project_path)

    match language_code:
        case "c":
            c.create_c_project(template)
        case "*":
            raise ClickException(f"{language_name} projects are currently unsupported.")
