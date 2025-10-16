// ============================================================================
// PROGRAMA: Ordenação Bubble Sort
// DESCRIÇÃO: Implementa algoritmo clássico de ordenação
// FUNCIONALIDADES TESTADAS:
//   - Múltiplas variáveis do mesmo tipo
//   - Loops aninhados (enquanto dentro de enquanto)
//   - Contadores e acumuladores
//   - Troca de valores entre variáveis
//   - Operações aritméticas e lógicas complexas
//   - Estruturas condicionais dentro de loops
// ============================================================================

inteiro num1, num2, num3, num4, num5;
inteiro i, j, temp, comparacoes, trocas;
logico houve_troca;

inicio
    escreva("============================================")
    escreva("      ALGORITMO DE ORDENAÇÃO BUBBLE SORT   ")
    escreva("============================================")
    escreva("")
    escreva("Este programa ordena 5 números em ordem crescente")
    escreva("usando o algoritmo Bubble Sort.")
    escreva("")
    
    // Entrada dos 5 números
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
    
    escreva("")
    escreva("--------------------------------------------")
    escreva("Números originais:", num1, num2, num3, num4, num5)
    escreva("--------------------------------------------")
    escreva("")
    
    // Inicialização dos contadores
    comparacoes <- 0
    trocas <- 0
    
    // Algoritmo Bubble Sort
    escreva("Iniciando ordenação...")
    escreva("")
    
    i <- 1
    enquanto i < 5 faca
        j <- 1
        houve_troca <- falso
        
        escreva("--- Iteração", i, "---")
        
        // Percorre o array fazendo comparações
        enquanto j <= 5 - i faca
            comparacoes <- comparacoes + 1
            
            // Comparação posição 1-2
            se j == 1 entao
                se num1 > num2 entao
                    escreva("  Trocando:", num1, "<->", num2)
                    temp <- num1
                    num1 <- num2
                    num2 <- temp
                    trocas <- trocas + 1
                    houve_troca <- verdadeiro
                fimse
            senao
                // Comparação posição 2-3
                se j == 2 entao
                    se num2 > num3 entao
                        escreva("  Trocando:", num2, "<->", num3)
                        temp <- num2
                        num2 <- num3
                        num3 <- temp
                        trocas <- trocas + 1
                        houve_troca <- verdadeiro
                    fimse
                senao
                    // Comparação posição 3-4
                    se j == 3 entao
                        se num3 > num4 entao
                            escreva("  Trocando:", num3, "<->", num4)
                            temp <- num3
                            num3 <- num4
                            num4 <- temp
                            trocas <- trocas + 1
                            houve_troca <- verdadeiro
                        fimse
                    senao
                        // Comparação posição 4-5
                        se j == 4 entao
                            se num4 > num5 entao
                                escreva("  Trocando:", num4, "<->", num5)
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
        
        // Otimização: se não houve troca, já está ordenado
        se houve_troca == falso entao
            escreva("  Sem trocas - Array já ordenado!")
        fimse
        
        escreva("  Estado atual:", num1, num2, num3, num4, num5)
        escreva("")
        
        i <- i + 1
    fimenquanto
    
    // Resultados finais
    escreva("============================================")
    escreva("           ORDENAÇÃO CONCLUÍDA!            ")
    escreva("============================================")
    escreva("Números ordenados:", num1, num2, num3, num4, num5)
    escreva("")
    escreva("--- ESTATÍSTICAS ---")
    escreva("Total de comparações:", comparacoes)
    escreva("Total de trocas:", trocas)
    escreva("Iterações completas:", i - 1)
    escreva("")
    
    // Análise de complexidade
    escreva("--- ANÁLISE DE DESEMPENHO ---")
    se trocas == 0 entao
        escreva("Melhor caso: Os números já estavam ordenados!")
        escreva("Complexidade: O(n) - Linear")
    senao
        se trocas < 5 entao
            escreva("Caso otimizado: Poucos movimentos necessários")
            escreva("Complexidade próxima ao melhor caso")
        senao
            se trocas < 10 entao
                escreva("Caso médio: Quantidade moderada de movimentos")
                escreva("Complexidade: O(n²) - Quadrática")
            senao
                escreva("Pior caso: Muitos movimentos necessários")
                escreva("Os números estavam em ordem inversa")
                escreva("Complexidade: O(n²) - Quadrática máxima")
            fimse
        fimse
    fimse
    
    escreva("")
    escreva("============================================")
    escreva("  Algoritmo Bubble Sort finalizado!        ")
    escreva("============================================")
fim
