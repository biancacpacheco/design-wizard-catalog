from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

aux_function = len(python_dw.get_all_functions()) >= 2

print(aux_function)






