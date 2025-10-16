// Programa de exemplo simples - Arquivo padrão
// Este é o arquivo executado por padrão quando você usa: python compilar.py

inteiro x, y, resultado;
logico maior;

inicio
    escreva("=== PROGRAMA EXEMPLO ===")
    escreva("")
    
    x <- 10
    y <- 5
    
    resultado <- x + y
    maior <- x > y
    
    escreva("X =", x)
    escreva("Y =", y)
    escreva("Soma =", resultado)
    escreva("X > Y?", maior)
    escreva("")
    
    se maior entao
        escreva("X é maior que Y!")
    senao
        escreva("Y é maior ou igual a X")
    fimse
    
    escreva("")
    escreva("Para mais exemplos, veja a pasta 'exemplos/'")
fim
