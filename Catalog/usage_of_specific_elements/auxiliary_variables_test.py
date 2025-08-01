from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

assign_entities = python_dw.get_entities_by_type("assign")
function_names = python_dw.get_all_functions()

aux_vars = False

args = function_names[0].args.args
args_names = [i.arg for i in args]

for e in assign_entities:
    for t in e.ast_node.targets:
        if python_dw.verify_instance(t, "name"):
            if t.id not in args_names:
                body = e.get_body()
                if not python_dw.verify_instance(body, "list"):
                    aux_vars = True
                    break
                if python_dw.verify_instance(body, "binop"):
                    if (not python_dw.verify_instance(body.left, "list")) and (not python_dw.verify_instance(body.right, "list")):
                        aux_vars = True
                        break
                

print(aux_vars)            