import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()


for_entities = python_dw.get_entities_by_type("for")

check_fors = False

if len(for_entities) == 3:
    for f in for_entities:
        if not python_dw.design_get_callees_from_entity_relation(f.get_name(), 'HASLOOP'):
            check_fors = True

check_aux_arrays = False

if check_fors:
    
    aux_arrays = 0
    verified_arrays = []

    function_names = python_dw.get_all_functions()

    args = function_names[0].args.args
    args_names = [i.arg for i in args]

    assign_entities = python_dw.get_entities_by_type("assign")

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            if body not in verified_arrays:
                aux_arrays += 1
                verified_arrays.append(body)
        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
                for t in targets:
                    if (t.id not in args_names) and (body not in verified_arrays):
                        verified_arrays.append(body)
                        aux_arrays += 1
    if aux_arrays == 2:
        check_aux_arrays = True


print(check_aux_arrays and check_fors)


        