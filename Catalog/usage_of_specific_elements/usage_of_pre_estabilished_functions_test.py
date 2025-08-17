import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()


necessary_elements = ["range", "for"]
usage_of_necessary_elements = True

entities = python_dw.entities

for element in necessary_elements:
    if element not in entities:
        usage_of_necessary_elements = False
        break

print(usage_of_necessary_elements)
