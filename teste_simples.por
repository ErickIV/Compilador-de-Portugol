// Programa de teste simples para o compilador modularizado
inteiro x, y, resultado;
logico maior;

inicio
    x <- 10
    y <- 5
    resultado <- x + y
    maior <- x > y
    
    escreva("X =", x)
    escreva("Y =", y)
    escreva("Resultado =", resultado)
    escreva("X é maior que Y:", maior)
    
    se maior entao
        escreva("X realmente é maior!")
    senao
        escreva("Y é maior ou igual")
    fimse
fim