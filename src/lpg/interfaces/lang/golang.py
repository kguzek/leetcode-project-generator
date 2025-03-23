"""Project generator for the Go language."""

import re

from .base import BaseLanguageInterface

# Go function signature pattern
FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^\s*func\s+(?P<name>\w+)\((?P<params>[^)]*)\)\s+(?P<returnType>[^{]+)\s*{",
    flags=re.MULTILINE,
)


TEST_FILE_TEMPLATE = """\
package main

import (
    "fmt"
)

func main() {{
    // Test case setup
    {params_setup}
    
    // Execute solution
    {result_var_declaration}{name}({params_call})
    
    // Display result
    fmt.Printf("{OUTPUT_RESULT_PREFIX} %v\\n", {result_var})
}}
"""
SOLUTION_REPLACEMENT_PATTERN = re.compile(r"\n}")
SOLUTION_REPLACEMENT_TEMPLATE = "{return_statement}\n}}"


class GoLanguageInterface(BaseLanguageInterface):
    """Implementation of the Go language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    test_command = ["./test"]

    @property
    def compile_command(self):
        args = ["go", "build", "-o", "test", "test.go", "solution.go"]

        supplemental_filename = self.get_supplemental_filename()
        if supplemental_filename is not None:
            args.append(supplemental_filename)

        return args

    def get_supplemental_filename(self):
        """Obtains the name of the supplemental file."""
        return "extra.go" if self.groups["supplemental_code"] else None

    @property
    def default_output(self):

        if self.is_void_return_type():
            return "0"
        if "[]" in self.groups["returnType"]:
            return "[]"
        output = self._get_default_value(self.groups["returnType"])
        # Converts the Go type to its string representation
        match output:
            case '""':
                return ""
            case "nil":
                return "<nil>"
            case _:
                return output

    def is_void_return_type(self):
        return self.groups["returnType"].strip() == ""

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
                self._get_variable_declaration(name, param_type)
                for name, param_type in zip(param_names, param_types)
            ]
        )

        self.groups["params_call"] = ", ".join(param_names)
        self.groups["return_statement"] = self._get_default_return(
            self.groups["returnType"]
        )

        # Handle non-void return types
        formatted_template = self.get_formatted_nonvoid_template(
            template,
            lambda: re.sub(
                SOLUTION_REPLACEMENT_PATTERN,
                (SOLUTION_REPLACEMENT_TEMPLATE.format(**self.groups)),
                template,
            ),
            "result := ",
        )

        project_files = {
            "solution.go": f"package main\n\n{formatted_template}",
            "test.go": TEST_FILE_TEMPLATE.format(**self.groups),
        }
        if self.groups["supplemental_code"]:
            filename = self.get_supplemental_filename()
            project_files[filename] = (
                f"package main\n\n{self.groups["supplemental_code"]}"
            )
        return project_files

    def _get_variable_declaration(self, name: str, variable_type: str) -> str:
        default_value = self._get_default_value(variable_type)
        if default_value == "nil":
            return f"var {name} {variable_type}"
        return f"{name} := {default_value}"

    def _get_default_value(self, param_type: str) -> str:
        """Returns a default value for the given Go type."""
        param_type = param_type.strip()

        switch_dict = {
            "int": "0",
            "float": "0.0",
            "double": "0.0",
            "string": '""',
            "bool": "false",
        }

        if "[]" in param_type:
            return f"{param_type}{{}}"  # Default slice initialization

        # Check for specific patterns
        if "map" in param_type or "*" in param_type:
            return "nil"

        # Check for simple matches in dictionary
        for key, value in switch_dict.items():
            if key in param_type:
                return value

        return f"{param_type}{{}}"  # Default struct initialization

    def _get_default_return(self, return_type: str) -> str:
        """Returns a default return statement for the given Go return type."""
        return_type = return_type.strip()

        if return_type == "":
            return ""  # No return for void functions

        default_value = self._get_default_value(return_type)
        return f"return {default_value}"
