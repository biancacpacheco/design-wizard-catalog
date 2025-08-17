import sys
from api.design_wizard import PythonDW

if len(sys.argv) != 2:
    print("Usage: python3 script.py path/to/file.py")
    sys.exit(1)

script_path = sys.argv[1]

python_dw = PythonDW()
python_dw.parse(script_path)
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