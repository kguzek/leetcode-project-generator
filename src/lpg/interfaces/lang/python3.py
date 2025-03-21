"""Project generator for the Python 3 language."""

import re
from .base import BaseLanguageInterface

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^def (?P<name>\w+)\((?P<params>[\w\s,=]*)\) -> (?P<returnType>\w+):$",
    flags=re.MULTILINE,
)

TEST_FILE_TEMPLATE = """\
if __name__ == "__main__":
    {params_setup}
    result = {name}({params_call})
    print("result:", result)
"""

class Python3LanguageInterface(BaseLanguageInterface):
    """Implementation of the Python 3 language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN

    def write_project_files(self, template: str):
        """Creates the project template for Python 3."""

        with open("solution.py", "w", encoding="utf-8") as file:
            file.write(template + "\n")

        params = self.groups["params"].split(", ") if self.groups["params"] else []
        self.groups["params_setup"] = "\n    ".join(
            f"{param.split('=')[0]} = 0" for param in params if param
        )
        self.groups["params_call"] = ", ".join(param.split('=')[0] for param in params)

        formatted = TEST_FILE_TEMPLATE.format(**self.groups)

        with open("test.py", "w", encoding="utf-8") as file:
            file.write(formatted)

