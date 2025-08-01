from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

list_usage = False

list_usage = len(python_dw.get_entities_by_type("list")) != 0

if not list_usage:
    assign_entities = python_dw.get_entities_by_type("assign")

    for e in assign_entities:
        body = e.get_body()
        if python_dw.verify_instance(body, "list"):
            list_usage = True
            break

        elif python_dw.verify_instance(body, "binop"):
            targets = e.ast_node.targets 
            if python_dw.verify_instance(body.left,"list") or (python_dw.verify_instance(body.right,"list")):
                for t in targets:
                    list_usage = True
                    break
        elif python_dw.verify_instance(body, "tuple"):
            for v in body.elts:
                if python_dw.verify_instance(v, "subscript") or python_dw.verify_instance(v,"list"):
                    list_usage = True
                    break
            if list_usage:
                break
        else:
            targets = e.ast_node.targets
            for t in targets:
                if python_dw.verify_instance(t, "subscript") or python_dw.verify_instance(t, "list"):
                    list_usage = True
                    break
                                
print(list_usage)

