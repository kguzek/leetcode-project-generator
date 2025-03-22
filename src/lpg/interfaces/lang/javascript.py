"""Project generator for the JavaScript language."""

import re

from .base import BaseLanguageInterface

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^var (?P<name>\w+) =(?P<async> async)? function\((?P<params>[^)]*?)(?:\.\.\.\w+)?\) \{$",
    flags=re.MULTILINE,
)

TEST_FILE_TEMPLATE = """\
import solution from "./solution.js";
{params_setup}
const result = {await}solution({params});
console.log("{OUTPUT_RESULT_PREFIX}", result);
"""


class JavaScriptLanguageInterface(BaseLanguageInterface):
    """Implementation of the JavaScript language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    compile_command = None
    test_command = ["node", "test.js"]
    default_output = "undefined"

    def prepare_project_files(self, template: str):
        self.groups["params_setup"] = ""
        for param in self.groups["params"].split(", "):
            if param.strip():
                self.groups["params_setup"] += f"\nconst {param} = undefined;"
        self.groups["await"] = "await " if self.groups["async"] else ""
        return {
            "solution.js": f"{template}\nexport default {self.groups['name']};",
            "test.js": TEST_FILE_TEMPLATE.format(**self.groups),
        }
