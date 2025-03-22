"""Project generator for the Python 2 language."""

import re

from .base import BaseLanguageInterface

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^\s*def (?P<name>\w+)\((?P<params>[^)]*)\):$",
    flags=re.MULTILINE,
)

TEST_FILE_TEMPLATE = """\
from solution import Solution

{supplemental_code}if __name__ == "__main__":
    {params_setup}
    result = Solution().{name}({params_call})
    print("{OUTPUT_RESULT_PREFIX}", result)
"""


class PythonLanguageInterface(BaseLanguageInterface):
    """Implementation of the Python 2 language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    compile_command = None
    test_command = ["python", "test.py"]
    default_output = "None"

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
        supplemental_code = self.add_newline(self.groups["supplemental_code"], 2)
        self.groups["supplemental_code"] = self.add_newline(
            self.groups["supplemental_code"], 2, "\n"
        )
        return {
            "solution.py": f"{supplemental_code}{template}pass\n",
            "test.py": TEST_FILE_TEMPLATE.format(**self.groups),
        }
