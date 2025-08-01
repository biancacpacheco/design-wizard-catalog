from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

necessary_elements = ["range", "for"]
usage_of_necessary_elements = True

entities = python_dw.entities

for element in necessary_elements:
    if element not in entities:
        usage_of_necessary_elements = False
        break

print(usage_of_necessary_elements)
