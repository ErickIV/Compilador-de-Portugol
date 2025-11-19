// ============================================================================
// PROGRAMA: Cálculo de Fatorial e Potência
// DESCRIÇÃO: Calcula fatorial e demonstra operador de potenciação
// FUNCIONALIDADES TESTADAS:
//   - Loop 'para' (novo!)
//   - Operador de potenciação ^ (novo!)
//   - Variáveis inteiras e reais
//   - Operações aritméticas
//   - Entrada e saída de dados
// ============================================================================

inteiro n, i, fatorial;
real base, expoente, potencia;

inicio
    escreva("============================================")
    escreva("   CALCULADORA MATEMÁTICA AVANÇADA")
    escreva("============================================")
    escreva("")

    // ========================================
    // PARTE 1: CÁLCULO DE FATORIAL
    // ========================================
    escreva("--- PARTE 1: FATORIAL ---")
    escreva("")
    escreva("Digite um número para calcular o fatorial: ")
    leia(n)

    se n < 0 entao
        escreva("ERRO: Fatorial não existe para números negativos!")
    senao
        se n > 12 entao
            escreva("AVISO: Números muito grandes podem causar overflow!")
            escreva("Limitando a 12.")
            n <- 12
        fimse

        // Calcular fatorial usando loop 'para'
        fatorial <- 1

        se n == 0 entao
            escreva("")
            escreva("Resultado: 0! = 1")
            escreva("(Por definição, o fatorial de 0 é 1)")
        senao
            para i de 1 ate n passo 1 faca
                fatorial <- fatorial * i
            fimpara

            escreva("")
            escreva("Resultado:", n, "! =", fatorial)
        fimse
    fimse

    escreva("")
    escreva("--------------------------------------------")

    // ========================================
    // PARTE 2: CÁLCULO DE POTÊNCIA
    // ========================================
    escreva("")
    escreva("--- PARTE 2: POTENCIAÇÃO (Operador ^) ---")
    escreva("")

    escreva("Digite a base: ")
    leia(base)

    escreva("Digite o expoente: ")
    leia(expoente)

    // Usar o novo operador de potenciação ^
    potencia <- base ^ expoente

    escreva("")
    escreva("Resultado:", base, "^", expoente, "=", potencia)

    // Exemplos adicionais de potenciação
    escreva("")
    escreva("--- EXEMPLOS DE POTENCIAÇÃO ---")
    escreva("2 ^ 3 =", 2.0 ^ 3.0)
    escreva("10 ^ 2 =", 10.0 ^ 2.0)
    escreva("5 ^ 0 =", 5.0 ^ 0.0)
    escreva("2 ^ 10 =", 2.0 ^ 10.0, "(1 kilobyte)")

    escreva("")
    escreva("--------------------------------------------")

    // ========================================
    // PARTE 3: APLICAÇÕES MATEMÁTICAS
    // ========================================
    escreva("")
    escreva("--- APLICAÇÕES MATEMÁTICAS ---")
    escreva("")

    // Área de um círculo usando potência
    real raio, area, pi;
    pi <- 3.14159

    escreva("Cálculo da área de um círculo:")
    escreva("Digite o raio: ")
    leia(raio)

    // Área = π × r²  (usando operador ^)
    area <- pi * (raio ^ 2.0)

    escreva("Área = π × r²")
    escreva("Área = 3.14159 ×", raio, "²")
    escreva("Área =", area)

    escreva("")
    escreva("============================================")
    escreva("  Cálculos concluídos!")
    escreva("============================================")
    escreva("")
    escreva("NOVOS RECURSOS DEMONSTRADOS:")
    escreva("✓ Loop 'para' com contador")
    escreva("✓ Operador de potenciação (^)")
    escreva("✓ Algoritmos matemáticos clássicos")
fim
