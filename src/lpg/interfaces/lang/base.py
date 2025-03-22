"""This file contains the base class for language interfaces."""

import re
from abc import ABCMeta, abstractmethod
from typing import Any, Match, Pattern

from ...constants import OUTPUT_RESULT_PREFIX

SUPPLEMENTAL_CODE_PATTERN = re.compile(
    r"Definition for .+\n(?:(?:# | \* |// ).+\n)+", re.MULTILINE
)
COMMENT_PATTERN = re.compile(r"^(?:# | \* |// )(.+)$")


class BaseLanguageInterface(metaclass=ABCMeta):
    """Base class for language interfaces."""

    def __init__(self):
        self.match = Match[str] | None
        self.groups: dict[str, str | Any] = {}

    @property
    @abstractmethod
    def function_signature_pattern(self) -> Pattern[str]:
        """The regular expression pattern which extracts data from the function definition."""

    @property
    @abstractmethod
    def compile_command(self) -> list[str] | None:
        """The command to compile the project, for testing. Can be set to None if not needed."""

    @property
    @abstractmethod
    def test_command(self) -> list[str]:
        """The command to run the project test."""

    @property
    @abstractmethod
    def default_output(self) -> str:
        """The default output when running the barebones project test."""

    @abstractmethod
    def prepare_project_files(self, template: str) -> dict[str, str]:
        """Generates a dictionary of filenames to file contents."""

    def create_project(self, template: str) -> None:
        """Writes the appropriate project template files in the current directory."""
        self.match = self.function_signature_pattern.search(template)
        if self.match is None:
            raise RuntimeError(
                f"Fatal error: project template doesn't match regex:\n\n{template}"
            )
        self.groups = self.match.groupdict()
        self.groups["OUTPUT_RESULT_PREFIX"] = OUTPUT_RESULT_PREFIX
        self.groups["supplemental_code"] = self.add_newline(
            self.get_supplemental_code(template)
        )

        for filename, content in self.prepare_project_files(template).items():
            with open(filename, "w", encoding="utf-8") as file:
                file.write(content)

    def get_supplemental_code(self, template: str) -> str | None:
        """Returns the implicit template code, such as a linked list node implementation."""
        match = SUPPLEMENTAL_CODE_PATTERN.search(template)
        if match is None:
            return None
        commented_code = match.group(0).split("\n")
        # the first line does not contain code
        commented_code.pop(0)
        return "\n".join(
            match.group(1)
            for match in (COMMENT_PATTERN.match(line) for line in commented_code)
            if match is not None
        )

    def add_newline(
        self, value: str | None, num_newlines: int = 1, prefix: str = ""
    ) -> str:
        """If the value is a non-empty string, adds the specified number of newline
        characters at the end (default 1). Adds the optional prefix before the value."""
        if not int.is_integer(num_newlines):
            raise ValueError("The number of newlines must be an integer.")
        if num_newlines < 1:
            raise ValueError("The number of newlines must be at least 1.")
        return f"{prefix}{value}{'\n' * num_newlines}" if value else ""
