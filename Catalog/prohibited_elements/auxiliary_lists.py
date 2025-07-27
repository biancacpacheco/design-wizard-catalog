from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("tests/data/auxiliary.py")
python_dw.design_populate_all_entities()

assign_entities = python_dw.get_entities_by_type("assign")

function_names = python_dw.get_all_functions()

#function.args: retorna objeto ast.arguments
#function.args.args: lista de argumentos
#function.args.args.arg: o nome do argumento 

args = function_names[0].args.args
args_names = [i.arg for i in args]

aux_structure = False

for e in assign_entities:
    body = e.get_body()
    if python_dw.verify_instance(body, "list"):
        aux_structure = True
        break

    elif python_dw.verify_instance(body, "binop"):
        targets = e.ast_node.targets 
        if python_dw.verify_instance(body.left,"list"):
            for t in targets:
                if t.id not in args_names:
                    aux_structure = True
                    break
        if ((not aux_structure) and (python_dw.verify_instance(body.left,"list"))):
            for t in targets:
                if t.id not in args_names:
                    aux_structure = True
                    break                               
    
print(aux_structure)
       