"""Project generator for the Python 3 language."""

import re
from .base import BaseLanguageInterface

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^(class Solution:\n)?\s*def (?P<name>\w+)\((?P<params>[^)]*)\) -> (?P<returnType>[^:]+):$",
    flags=re.MULTILINE,
)

# LeetCode uses Typing types, not Python 3.9+ types
TYPING_IMPORT_TEMPLATE = "from typing import *\n\n"

TEST_FILE_TEMPLATE = """\
from solution import Solution


if __name__ == "__main__":
    {params_setup}
    result = Solution().{name}({params_call})
    print("result:", result)
"""


class Python3LanguageInterface(BaseLanguageInterface):
    """Implementation of the Python 3 language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN

    def prepare_project_files(self, template: str):
        params = (
            [
                param
                for param in self.groups["params"].split(", ")
                if param and param != "self"
            ]
            if self.groups["params"]
            else []
        )
        self.groups["params_setup"] = "\n    ".join(
            param if "=" in param else f"{param} = None" for param in params
        )
        self.groups["params_call"] = ", ".join(
            param.split("=")[0].split(":")[0].strip() for param in params
        )

        return {
            "solution.py": f"{TYPING_IMPORT_TEMPLATE}\n{template}pass\n",
            "test.py": f"{TYPING_IMPORT_TEMPLATE}{TEST_FILE_TEMPLATE.format(**self.groups)}",
        }
