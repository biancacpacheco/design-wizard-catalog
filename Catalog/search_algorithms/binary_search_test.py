import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
python_dw.design_populate_all_entities()


while_usage = len(python_dw.get_entities_by_type("while")) == 1

aux_var = []

if while_usage:
    
    assign_entities = python_dw.get_entities_by_type("assign")
    function_names = python_dw.get_all_functions()
    
    args = function_names[0].args.args
    args_names = [i.arg for i in args]

    for e in assign_entities:
        for t in e.ast_node.targets:
            if python_dw.verify_instance(t, "name"):
                if t.id not in args_names:
                    body = e.get_body()
                    if not python_dw.verify_instance(body, "list"):
                        if t.id not in aux_var:
                            aux_var.append(t.id)
                    if python_dw.verify_instance(body, "binop"):
                        if (not python_dw.verify_instance(body.left, "list")) and (not python_dw.verify_instance(body.right, "list")):
                            if t.id not in aux_var:
                                aux_var.append(t.id)


binary_search = while_usage and len(aux_var) == 3

print(binary_search)