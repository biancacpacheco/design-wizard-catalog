from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("tests/data/bubblesort.py")
python_dw.design_populate_all_entities()

for_entities = python_dw.get_entities_by_type('for')

bubble = False

if len(for_entities) == 2:
    relations = python_dw.design_get_callees_from_entity_relation('for1', 'HASLOOP')
    if len(relations) > 0:
        if relations[0].get_name() == for_entities[1].get_name():
            bubble = True

print(bubble)