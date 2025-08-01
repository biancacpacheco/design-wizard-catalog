from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

conditionals = len(python_dw.get_entities_by_type("if")) > 0 

print(conditionals)
