// ============================================================================
// PROGRAMA: Sequência de Fibonacci
// DESCRIÇÃO: Calcula os primeiros N números da sequência de Fibonacci
// FUNCIONALIDADES TESTADAS:
//   - Loop 'para' (novo!)
//   - Variáveis inteiras
//   - Operações aritméticas
//   - Entrada e saída de dados
//   - Algoritmo iterativo clássico
// ============================================================================

inteiro n, i, fib_anterior, fib_atual, proximo;

inicio
    escreva("============================================")
    escreva("   SEQUÊNCIA DE FIBONACCI")
    escreva("============================================")
    escreva("")
    escreva("Este programa calcula os primeiros N números")
    escreva("da sequência de Fibonacci.")
    escreva("")

    // Entrada do usuário
    escreva("Quantos números deseja calcular? (máx 20): ")
    leia(n)

    // Validação
    se n <= 0 entao
        escreva("ERRO: Digite um número maior que zero!")
    senao
        se n > 20 entao
            escreva("AVISO: Limitando a 20 números.")
            n <- 20
        fimse

        escreva("")
        escreva("--------------------------------------------")
        escreva("  SEQUÊNCIA DE FIBONACCI - Primeiros", n, "números")
        escreva("--------------------------------------------")
        escreva("")

        // Inicializar os dois primeiros números
        fib_anterior <- 0
        fib_atual <- 1

        // Exibir primeiro número
        se n >= 1 entao
            escreva("Fibonacci(1) =", fib_anterior)
        fimse

        // Exibir segundo número
        se n >= 2 entao
            escreva("Fibonacci(2) =", fib_atual)
        fimse

        // Calcular e exibir os demais usando loop 'para'
        se n > 2 entao
            para i de 3 ate n passo 1 faca
                proximo <- fib_anterior + fib_atual
                escreva("Fibonacci(", i, ") =", proximo)

                // Atualizar para próxima iteração
                fib_anterior <- fib_atual
                fib_atual <- proximo
            fimpara
        fimse

        escreva("")
        escreva("============================================")
        escreva("  Cálculo concluído!")
        escreva("============================================")
        escreva("")
        escreva("CURIOSIDADE: A sequência de Fibonacci")
        escreva("aparece em padrões da natureza como")
        escreva("conchas, flores e galáxias!")
    fimse
fim
