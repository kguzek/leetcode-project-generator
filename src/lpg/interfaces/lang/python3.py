"""Project generator for the Python 3 language."""

import re

from .python import PythonLanguageInterface

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^\s*def (?P<name>\w+)\((?P<params>[^)]*)\) -> (?P<returnType>[^:]+):$",
    flags=re.MULTILINE,
)


# LeetCode uses Typing types, not Python 3.9+ types
TYPING_IMPORT_TEMPLATE = "from typing import *\n\n"


class Python3LanguageInterface(PythonLanguageInterface):
    """Implementation of the Python 3 language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN

    def prepare_project_files(self, template):
        project_files = super().prepare_project_files(template)
        return {
            "solution.py": f"{TYPING_IMPORT_TEMPLATE}\n{project_files['solution.py']}",
            "test.py": f"{TYPING_IMPORT_TEMPLATE}{project_files['test.py']}",
        }
