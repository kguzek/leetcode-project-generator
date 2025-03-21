"""This file contains the base class for language interfaces."""

from abc import abstractmethod
from typing import Any, Pattern, Match


class BaseLanguageInterface:
    """Base class for language interfaces."""

    def __init__(self):
        self.match = Match[str] | None
        self.groups: dict[str, str | Any] = {}

    @property
    @abstractmethod
    def function_signature_pattern(self) -> Pattern[str]:
        """Returns the function signature regular expression pattern."""

    @abstractmethod
    def prepare_project_files(self, template: str) -> dict[str, str]:
        """Generates a dictionary of filenames to file contents."""

    def create_project(self, template: str) -> None:
        """Creates the project template."""
        self.match = self.function_signature_pattern.search(template)
        if self.match is None:
            raise RuntimeError(
                f"Fatal error: project template doesn't match regex:\n\n{template}"
            )
        self.groups = self.match.groupdict()

        for filename, content in self.prepare_project_files(template).items():
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)
