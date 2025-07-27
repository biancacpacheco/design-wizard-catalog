from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("tests/data/notnicefunction.py")
python_dw.design_populate_all_entities()

prohibited_functions = ["sort", "split", "issubset", "issuperset", "union", "intersection", "difference", "join", "symmetric_difference"] 
allowed_function = True

for function in prohibited_functions:
    if python_dw.get_entities_by_type(function) != []:
        allowed_function = False

print(allowed_function)
