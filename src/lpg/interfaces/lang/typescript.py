"""Project generator for the TypeScript language."""

import re

from .javascript import JavaScriptLanguageInterface

FUNCTION_SIGNATURE_PATTERN = re.compile(
    r"^(?P<async>async )?function (?P<name>\w+)\((?P<params>[^)]*?)(?:\.\.\.[^)]+)?\): [^{]+ \{$",
    flags=re.MULTILINE,
)

TYPE_DECLARATION_PATTERN = re.compile(r"^type \w+ = .+$", re.MULTILINE)


class TypeScriptLanguageInterface(JavaScriptLanguageInterface):
    """Implementation of the TypeScript language project template interface."""

    function_signature_pattern = FUNCTION_SIGNATURE_PATTERN
    compile_command = ["tsc", "--noCheck", "--module", "preserve", "test.ts"]
    test_command = ["node", "test.js"]

    def prepare_project_files(self, template: str):
        untyped_params = ", ".join(
            param.split(":")[0].strip()
            for param in self.groups["params"].split(", ")
            if param.strip()
        )
        self.groups["params"] = untyped_params
        type_declarations = TYPE_DECLARATION_PATTERN.findall(template)
        project_files = super().prepare_project_files(template)
        test_file_contents = project_files["test.js"]
        if len(type_declarations) > 0:
            test_file_contents = (
                f"{'\n'.join(type_declarations)}\n\n{test_file_contents}"
            )
        supplemental_code = self.add_newline(self.groups["supplemental_code"])
        return {
            "solution.ts": f"{supplemental_code}{project_files['solution.js']}",
            "test.ts": test_file_contents,
        }
