from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("tests/data/notnicefunction.py")
python_dw.design_populate_all_entities()

prohibited_structures = ["dict", "set"]

assign_entities = python_dw.get_entities_by_type('assign')

allowed_structures = True

for node in assign_entities:
    for struct in prohibited_structures:
        if python_dw.verify_instance(node.get_body(), struct):
            allowed_structures = False
            break

print(allowed_structures)

