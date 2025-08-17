import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()


merge_sort = True
while_entities = python_dw.get_entities_by_type("while")


if (not len(while_entities) == 2 and not len(while_entities) == 3):
    merge_sort = False

if merge_sort:
    functions = python_dw.get_all_functions()
    if len(functions) < 2:
        merge_sort = False

aux_structure = False

if merge_sort:
    arguments = functions[0].args.args
    args_names = [a.arg for a in arguments]

    assign_entities = python_dw.get_entities_by_type("assign")

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            aux_structure = True
            break

        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
                for t in targets:
                    if t.id not in args_names:
                        aux_structure = True
                        break

if not aux_structure:
    merge_sort = False 

print(merge_sort)
