from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

for_usage = len(python_dw.get_entities_by_type("for")) > 0 
while_usage = len(python_dw.get_entities_by_type("while")) > 0

exclusively_for = for_usage and not while_usage

print(exclusively_for)
