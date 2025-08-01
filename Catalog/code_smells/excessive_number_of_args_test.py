from api.design_wizard import PythonDW

python_dw = PythonDW()
python_dw.parse("path/to/script.py")
python_dw.design_populate_all_entities()

functions= python_dw.get_all_functions()

#function.args: retorna objeto ast.arguments
#function.args.args: lista de argumentos
#function.args.args.arg: o nome do argumento 

## verifica um tamanho limite pra cada função - pode ser adaptado para casos especificos em que o
## aluno cria multiplas funções e a quantidade de parametros de cada uma é pre-determinado.
arg_limit = 5
accepted_number_of_args = True

for f in range(len(functions)):
    args = functions[f].args.args
    
    if len(args) > arg_limit:
        accepted_number_of_args = False
        break

print(accepted_number_of_args)
