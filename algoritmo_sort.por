// Programa algoritmo: Ordenação Bubble Sort
// Demonstra algoritmos clássicos e manipulação de dados

// Declarações de variáveis
inteiro tamanho, i, j, temp, trocas, comparacoes;
inteiro num1, num2, num3, num4, num5; // simulando array
logico houve_troca;

inicio

    escreva("=== ALGORITMO BUBBLE SORT ===")
    escreva("Este programa ordena 5 números em ordem crescente")
    
    // Entrada dos dados
    escreva("Digite o 1º número: ")
    leia(num1)
    escreva("Digite o 2º número: ")
    leia(num2)
    escreva("Digite o 3º número: ")
    leia(num3)
    escreva("Digite o 4º número: ")
    leia(num4)
    escreva("Digite o 5º número: ")
    leia(num5)
    
    escreva("Números originais: ", num1, ", ", num2, ", ", num3, ", ", num4, ", ", num5)
    
    // Inicialização
    tamanho <- 5
    trocas <- 0
    comparacoes <- 0
    
    // Algoritmo Bubble Sort (simulado com variáveis individuais)
    i <- 1
    enquanto (i < tamanho) faca
        j <- 1
        houve_troca <- falso
        
        enquanto (j <= tamanho - i) faca
            comparacoes <- comparacoes + 1
            
            // Comparação e troca para posição 1-2
            se (j == 1) entao
                se (num1 > num2) entao
                    temp <- num1
                    num1 <- num2
                    num2 <- temp
                    trocas <- trocas + 1
                    houve_troca <- verdadeiro
                fimse
            senao
                // Comparação e troca para posição 2-3
                se (j == 2) entao
                    se (num2 > num3) entao
                        temp <- num2
                        num2 <- num3
                        num3 <- temp
                        trocas <- trocas + 1
                        houve_troca <- verdadeiro
                    fimse
                senao
                    // Comparação e troca para posição 3-4
                    se (j == 3) entao
                        se (num3 > num4) entao
                            temp <- num3
                            num3 <- num4
                            num4 <- temp
                            trocas <- trocas + 1
                            houve_troca <- verdadeiro
                        fimse
                    senao
                        // Comparação e troca para posição 4-5
                        se (j == 4) entao
                            se (num4 > num5) entao
                                temp <- num4
                                num4 <- num5
                                num5 <- temp
                                trocas <- trocas + 1
                                houve_troca <- verdadeiro
                            fimse
                        fimse
                    fimse
                fimse
            fimse
            
            j <- j + 1
        fimenquanto
        
        // Se não houve troca, já está ordenado
        se (houve_troca == falso) entao
            escreva("Array já ordenado na iteração ", i)
        fimse
        
        i <- i + 1
    fimenquanto
    
    escreva("Números ordenados: ", num1, ", ", num2, ", ", num3, ", ", num4, ", ", num5)
    escreva("Total de comparações: ", comparacoes)
    escreva("Total de trocas: ", trocas)
    
    // Análise dos resultados
    se (trocas == 0) entao
        escreva("Análise: Os números já estavam ordenados!")
    senao
        se (trocas < 5) entao
            escreva("Análise: Poucos movimentos necessários")
        senao
            se (trocas < 10) entao
                escreva("Análise: Moderada quantidade de movimentos")
            senao
                escreva("Análise: Muitos movimentos necessários")
            fimse
        fimse
    fimse
    
    escreva("Algoritmo Bubble Sort concluído!")
fim