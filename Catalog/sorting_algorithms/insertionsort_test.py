from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

for_entities = python_dw.get_entities_by_type('for')
while_entities = python_dw.get_entities_by_type('while')

insertion = False

if len(for_entities) == 1 and len(while_entities) == 1:
    relations = python_dw.design_get_callees_from_entity_relation('for1', 'HASLOOP')
    if len(relations) > 0:
        if relations[0].get_name() == while_entities[0].get_name():
            insertion = True

print(insertion)