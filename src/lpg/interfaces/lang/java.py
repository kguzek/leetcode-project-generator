"""Project generator for the Java language."""

import re

from .base import BaseLanguageInterface

TEST_FILE_TEMPLATE = """\

public class Test {{
    public static void main(String[] args) {{
        {params_setup};
        {result_var_declaration}new Solution().{name}({params_call});
        System.out.printf("{OUTPUT_RESULT_PREFIX} %s\\n", {result_var});
    }}
}}
"""

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"public (?P<returnType>[^\s]+) (?P<name>\w+(?:\[\]|\s?\*+)?)\((?P<params>[^)]*)\)\s?{$",
    flags=re.MULTILINE,
)


SOLUTION_REPLACEMENT_PATTERN = re.compile(r"\n    }")
SOLUTION_REPLACEMENT_TEMPLATE = "return {return_value};\n    }}"
SUPPLEMENTAL_FILENAME_PATTERN = re.compile(r"public class (\w+) {")
UTIL_IMPORT_TEMPLATE = "import java.util.*;\n\n"


class JavaLanguageInterface(BaseLanguageInterface):
    """Implementation of the Java language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    test_command = ["java", "Test"]

    @property
    def compile_command(self):
        args = ["javac", "Solution.java", "Test.java"]

        supplemental_filename = self.get_supplemental_filename()
        if supplemental_filename is not None:
            args.append(supplemental_filename)

        return args

    @property
    def default_output(self):
        return self.get_default_value(self.groups["returnType"])

    def get_supplemental_filename(self):
        """Obtains the name of the supplemental file."""
        code = self.groups["supplemental_code"]
        if not code:
            return None
        return f"{SUPPLEMENTAL_FILENAME_PATTERN.search(code).group(1)}.java"

    def get_default_value(self, variable_type: str):
        """Obtains the default value for a given variable type."""
        return {"boolean": "false", "int": "0", "void": "0"}.get(variable_type, "null")

    def prepare_project_files(self, template: str):
        params = self.groups["params"].split(", ")
        self.groups["params_setup"] = ";\n        ".join(
            f"{param} = {self.get_default_value(param.split()[0])}"
            for param in self.groups["params"].split(", ")
        )
        self.groups["params_call"] = ", ".join(param.split()[-1] for param in params)

        formatted_template = self.get_formatted_nonvoid_template(
            template,
            lambda: re.sub(
                SOLUTION_REPLACEMENT_PATTERN,
                SOLUTION_REPLACEMENT_TEMPLATE.format(return_value=self.default_output),
                template,
            ),
        )

        project_files = {
            "Solution.java": f"{UTIL_IMPORT_TEMPLATE}{formatted_template}\n",
            "Test.java": UTIL_IMPORT_TEMPLATE
            + TEST_FILE_TEMPLATE.format(**self.groups),
        }
        if self.groups["supplemental_code"]:
            filename = self.get_supplemental_filename()
            project_files[filename] = self.groups["supplemental_code"]
        return project_files
