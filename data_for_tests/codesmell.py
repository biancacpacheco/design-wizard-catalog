def analisar_dados(a, b, c, d, e, f):
    
    if a + b > 100:
        return "A soma de a + b é maior que 100"
    
    if c - d < 0:
        return "A subtração c - d é negativa"
    
    if e * f == 0:
        return "O produto de e * f é zero"
    
    if a == b == c == d == e == f:
        return "Todos os valores são iguais"
    
    return "Nenhuma condição especial foi satisfeita"