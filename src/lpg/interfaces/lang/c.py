"""Project generator for the C language."""

import re
from .base import BaseLanguageInterface

HEADER_FILE_TEMPLATE = "{returnType} {name}({params});"

TEST_FILE_TEMPLATE = """\
#include <stdio.h>
#include "solution.h"

int main() {{
    {param_declarations};
    {returnType} result = {name}({params_call});
    printf("result: %d\\n", result);
    return 0;
}}
"""

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^(?P<returnType>(?:struct )?\w+(?:\[\]|\*\*?)?) (?P<name>\w+)\((?P<params>(?:(?:struct )?\w+(?:\[\]|\*\*?)? \w+(?:, )?)+)\)\s?{$",
    flags=re.MULTILINE,
)


class CLanguageInterface(BaseLanguageInterface):
    """Implementation of the C language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN

    def write_project_files(self, template: str):
        """Creates the project template for C."""

        with open("solution.c", "w", encoding="utf-8") as file:
            file.write(template + "\n")

        with open("solution.h", "w", encoding="utf-8") as file:
            file.write(HEADER_FILE_TEMPLATE.format(**self.groups))

        params = self.groups["params"].split(", ")
        self.groups["param_declarations"] = self.groups["params"].replace(
            ", ", ";\n    "
        )
        self.groups["params_call"] = ", ".join(param.split()[-1] for param in params)
        formatted = TEST_FILE_TEMPLATE.format(**self.groups)

        with open("test.c", "w", encoding="utf-8") as file:
            file.write(formatted)
