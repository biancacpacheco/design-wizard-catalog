import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()


conditionals = len(python_dw.get_entities_by_type("if")) > 0 

print(conditionals)
