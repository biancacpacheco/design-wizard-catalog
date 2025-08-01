from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

function_names = python_dw.get_all_functions()

args = function_names[0].args.args
args_names = [i.arg for i in args]

for_entities = python_dw.get_entities_by_type("for")

nestled_fors = False
aux_variable = False

if len(for_entities) == 2:
    relations = python_dw.design_get_callees_from_entity_relation('for1', 'HASLOOP')
    if len(relations) > 0:
        if relations[0].get_name() == for_entities[1].get_name():
            nestled_fors = True
        
    
    if (nestled_fors):
        body = for_entities[0].get_ast_node().body
        for node in body:
            if python_dw.verify_instance(node, "assign"):
                for t in node.targets:
                    if python_dw.verify_instance(t, "name"):
                        if t.id not in args_names:
                            aux_variable = True

print(nestled_fors and aux_variable)

