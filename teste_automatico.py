# Código gerado automaticamente do Portugol

def main():
    # Declarações de variáveis
    x = 0
    y = 0
    soma = 0
    media = 0.0
    maior = False
    
    x = 10
    y = 20
    soma = (x + y)
    media = (soma / 2)
    maior = (x > y)
    print("=== RESULTADOS ===")
    print("X =", x)
    print("Y =", y)
    print("Soma =", soma)
    print("Média =", media)
    print("X é maior que Y?", maior)
    if maior:
        print("X realmente é maior!")
    else:
        print("Y é maior ou igual a X")
    print("Programa finalizado!")

if __name__ == '__main__':
    main()