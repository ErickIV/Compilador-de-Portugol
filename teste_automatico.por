// Programa simples sem entrada do usuário
inteiro x, y, soma;
real media;
logico maior;

inicio
    x <- 10
    y <- 20
    soma <- x + y
    media <- soma / 2
    maior <- x > y
    
    escreva("=== RESULTADOS ===")
    escreva("X =", x)
    escreva("Y =", y)
    escreva("Soma =", soma)
    escreva("Média =", media)
    escreva("X é maior que Y?", maior)
    
    se maior entao
        escreva("X realmente é maior!")
    senao
        escreva("Y é maior ou igual a X")
    fimse
    
    escreva("Programa finalizado!")
fim