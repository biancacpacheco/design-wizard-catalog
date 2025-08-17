import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()


prohibited_structures = ["dict", "set"]

assign_entities = python_dw.get_entities_by_type('assign')

allowed_structures = True

for s in prohibited_structures:
    if s in python_dw.entities:
        allowed_structures = False
        break


if allowed_structures:
    for node in assign_entities:
        for struct in prohibited_structures:
            if python_dw.verify_instance(node.get_body(), struct):
                allowed_structures = False
                break
            else:
                for t in node.ast_node.targets:
                    if python_dw.verify_instance(t, struct):
                        allowed_structures = False
                        break

print(allowed_structures)



