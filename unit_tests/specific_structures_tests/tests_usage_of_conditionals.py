import unittest
import os
import subprocess

# Definindo o módulo que será testado via `python3 -m`
SCRIPT_MODULE = "catalog.usage_of_specific_elements.usage_of_conditionals_test"

class TestUsageOfPreEstablishedFunctions(unittest.TestCase):

    def run_script_with_file(self, file_path=None):
        """Executa o script como subprocesso e retorna stdout, stderr e código de saída."""
        command = ["python3", "-m", SCRIPT_MODULE]
        if file_path:
            command.append(file_path)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode

    def test_valid_example(self):
        data_file = os.path.join("tests", "data", "bubblesort.py")
        stdout, stderr, returncode = self.run_script_with_file(data_file)

        self.assertEqual(returncode, 0)
        self.assertEqual(stdout, "True")

    def test_missing_elements(self):
        data_file = os.path.join("tests", "data", "notnicefunction.py")
        stdout, stderr, returncode = self.run_script_with_file(data_file)

        self.assertEqual(returncode, 0)
        self.assertEqual(stdout, "False")

    def test_missing_argument(self):
        stdout, stderr, returncode = self.run_script_with_file()

        self.assertEqual(returncode, 1)
        self.assertIn("Usage:", stdout)

if __name__ == "__main__":
    unittest.main()

