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
    def write_project_files(self, template: str) -> None:
        """Writes the project files."""

    def create_project(self, template: str) -> None:
        """Creates the project template."""
        self.match = self.function_signature_pattern.search(template)
        if self.match is None:
            raise RuntimeError(
                f"Fatal error: project template doesn't match regex:\n\n{template}"
            )
        self.groups = self.match.groupdict()

        self.write_project_files(template)
