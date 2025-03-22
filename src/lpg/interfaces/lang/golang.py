"""Project generator for the Go language."""

import re
from .base import BaseLanguageInterface

# Go function signature pattern
FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^\s*func\s+(?P<name>\w+)\((?P<params>[^)]*)\)\s+(?P<returnType>[^{]+)\s*{",
    flags=re.MULTILINE,
)

SOLUTION_FILE_TEMPLATE = """\
package solution

{supplemental_code}
func {name}({params}) {returnType} {
    // TODO: Implement solution
    {return_statement}
}
"""

TEST_FILE_TEMPLATE = """\
package main

import (
    "fmt"
    "./solution"
)

func main() {
    // Test case setup
    {params_setup}
    
    // Execute solution
    {result_var_declaration}solution.{name}({params_call})
    
    // Display result
    fmt.Printf("{OUTPUT_RESULT_PREFIX} %v\\n", {result_var})
}
"""


class GoLanguageInterface(BaseLanguageInterface):
    """Implementation of the Go language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    compile_command = ["go", "build", "-o", "test", "test.go"]
    test_command = ["./test"]
    default_output = "0"

    def prepare_project_files(self, template: str):
        params = self.groups["params"].split(", ")
        param_names = []
        param_types = []

        for param in params:
            if not param.strip():
                continue

            parts = param.strip().split()
            if len(parts) == 2:
                param_names.append(parts[0])
                param_types.append(parts[1])
            else:
                # Handle unnamed parameters or complex types
                param_names.append(f"param{len(param_names)}")
                param_types.append(param.strip())

        self.groups["params_setup"] = ";\n    ".join(
            [
                f"{name} := {self._get_default_value(param_type)}"
                for name, param_type in zip(param_names, param_types)
            ]
        )

        self.groups["params_call"] = ", ".join(param_names)
        self.groups["return_statement"] = self._get_default_return(
            self.groups["returnType"]
        )

        # Handle non-void return types
        formatted_template = self.get_formatted_nonvoid_template(
            TEST_FILE_TEMPLATE, lambda: TEST_FILE_TEMPLATE
        )

        return {
            "solution/solution.go": SOLUTION_FILE_TEMPLATE.format(**self.groups),
            "test.go": formatted_template.format(**self.groups),
        }

    def _get_default_value(self, param_type: str) -> str:
        """Returns a default value for the given Go type."""
        param_type = param_type.strip()

        if "int" in param_type:
            return "0"
        elif "float" in param_type or "double" in param_type:
            return "0.0"
        elif "string" in param_type:
            return '""'
        elif "bool" in param_type:
            return "false"
        elif "[]" in param_type:  # array/slice
            return "nil"
        elif "map" in param_type:
            return "nil"
        elif "*" in param_type:  # pointer
            return "nil"
        else:
            return param_type + "{}"  # struct default

    def _get_default_return(self, return_type: str) -> str:
        """Returns a default return statement for the given Go return type."""
        return_type = return_type.strip()

        if return_type == "":
            return ""  # No return for void functions

        default_value = self._get_default_value(return_type)
        return f"return {default_value}"
