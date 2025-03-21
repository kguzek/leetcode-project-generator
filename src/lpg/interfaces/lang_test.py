"""Unit test for all language interfaces."""

import os
import subprocess
import tempfile
import unittest

from ..constants import OUTPUT_RESULT_PREFIX
from .file import LANGUAGE_INTERFACES
from .web import get_code_snippets

TEST_CASES = [
    "add-binary",
    "add-two-numbers",
    "add-two-promises",
    "build-array-from-permutation",
    "climbing-stairs",
    "concatenation-of-array",
    "defanging-an-ip-address",
    "display-the-first-three-rows",
    "divide-two-integers",
    "final-value-of-variable-after-performing-operations",
    "find-the-index-of-the-first-occurrence-in-a-string",
    "hand-of-straights",
    "integer-to-roman",
    "length-of-last-word",
    "longest-palindromic-substring",
    "longest-substring-without-repeating-characters",
    "merge-sorted-array",
    "merge-two-sorted-lists",
    "n-queens",
    "minimize-maximum-pair-sum-in-array",
    "modify-columns",
    "number-of-good-pairs",
    "plus-one",
    "remove-duplicates-from-sorted-list",
    "return-length-of-arguments-passed",
    "reverse-string",
    "score-of-a-string",
    "search-insert-position",
    "string-to-integer-atoi",
    "two-sum",
]


class TestProjectGeneration(unittest.TestCase):
    """Test case for the project generation process."""

    def conduct_tests(self, code_snippets: list[dict[str, str]]):
        """Generates, compiles and runs the solution code for each supported language."""
        for template_data in code_snippets:
            language = template_data["langSlug"]
            interface = LANGUAGE_INTERFACES.get(language)
            if interface is None:
                continue

            # print(f"Testing {language} interface...")
            interface.create_project(template_data["code"])
            if interface.compile_command is not None:
                subprocess.run(interface.compile_command, check=True)
            result = subprocess.run(
                interface.test_command, check=True, capture_output=True
            )
            self.assertMultiLineEqual(
                result.stdout.decode().strip(),
                f"{OUTPUT_RESULT_PREFIX} {interface.default_output}",
            )


def generate_test(test_case: str):
    """Generates a test function for a specific LeetCode problem."""

    def test(self: TestProjectGeneration):
        with tempfile.TemporaryDirectory() as temp_dir:
            # print(f"\nGenerating {test_case} in directory {temp_dir}...")
            os.chdir(temp_dir)
            self.conduct_tests(get_code_snippets(test_case))

    return test


def register_tests():
    """Registers all LeetCode problems as separate test cases."""
    for test_case in TEST_CASES:
        test_name = f"test_{test_case.replace('-', '_')}"
        setattr(TestProjectGeneration, test_name, generate_test(test_case))


register_tests()

if __name__ == "__main__":
    unittest.main()
