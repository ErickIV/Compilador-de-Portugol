// ============================================================================
// PROGRAMA: Teste do Operador Módulo (%)
// DESCRIÇÃO: Demonstra o uso do operador módulo para verificar paridade
// FUNCIONALIDADES TESTADAS:
//   - Operador módulo % (novo!)
//   - Loop 'para' (novo!)
//   - Condicionais
//   - Verificação de divisibilidade
// ============================================================================

inteiro numero, i, resto, divisor;
inteiro contadorPares, contadorImpares;

inicio
    escreva("============================================")
    escreva("   TESTE DO OPERADOR MÓDULO (%)")
    escreva("============================================")
    escreva("")
    escreva("O operador módulo (%) retorna o resto da divisão.")
    escreva("Útil para verificar divisibilidade e paridade!")
    escreva("")

    // ========================================
    // PARTE 1: TESTE DE PARIDADE
    // ========================================
    escreva("--- PARTE 1: VERIFICADOR PAR/ÍMPAR ---")
    escreva("")
    escreva("Digite um número: ")
    leia(numero)

    resto <- numero % 2

    escreva("")
    escreva("Número:", numero)
    escreva("Resto da divisão por 2:", resto)

    se resto == 0 entao
        escreva("Resultado: PAR ✓")
        escreva("(Divisível por 2)")
    senao
        escreva("Resultado: ÍMPAR ✓")
        escreva("(Não divisível por 2)")
    fimse

    escreva("")
    escreva("--------------------------------------------")

    // ========================================
    // PARTE 2: TESTE DE DIVISIBILIDADE
    // ========================================
    escreva("")
    escreva("--- PARTE 2: TESTE DE DIVISIBILIDADE ---")
    escreva("")
    escreva("Digite um número para testar: ")
    leia(numero)
    escreva("Digite o divisor: ")
    leia(divisor)

    se divisor == 0 entao
        escreva("ERRO: Divisão por zero!")
    senao
        resto <- numero % divisor

        escreva("")
        escreva(numero, "÷", divisor, "=", numero / divisor)
        escreva("Resto:", resto)

        se resto == 0 entao
            escreva("")
            escreva("✓", numero, "é divisível por", divisor)
        senao
            escreva("")
            escreva("✗", numero, "NÃO é divisível por", divisor)
        fimse
    fimse

    escreva("")
    escreva("--------------------------------------------")

    // ========================================
    // PARTE 3: ANÁLISE DE SEQUÊNCIA
    // ========================================
    escreva("")
    escreva("--- PARTE 3: ANÁLISE DE PARES E ÍMPARES ---")
    escreva("")
    escreva("Analisando números de 1 a 20:")
    escreva("")

    contadorPares <- 0
    contadorImpares <- 0

    para i de 1 ate 20 passo 1 faca
        resto <- i % 2

        se resto == 0 entao
            escreva(i, "- PAR")
            contadorPares <- contadorPares + 1
        senao
            escreva(i, "- ÍMPAR")
            contadorImpares <- contadorImpares + 1
        fimse
    fimpara

    escreva("")
    escreva("Estatísticas:")
    escreva("Total de pares:", contadorPares)
    escreva("Total de ímpares:", contadorImpares)

    escreva("")
    escreva("--------------------------------------------")

    // ========================================
    // PARTE 4: MÚLTIPLOS
    // ========================================
    escreva("")
    escreva("--- PARTE 4: ENCONTRAR MÚLTIPLOS ---")
    escreva("")
    escreva("Múltiplos de 3 entre 1 e 30:")
    escreva("")

    para i de 1 ate 30 passo 1 faca
        resto <- i % 3

        se resto == 0 entao
            escreva(i, "é múltiplo de 3")
        fimse
    fimpara

    escreva("")
    escreva("============================================")
    escreva("  Testes concluídos!")
    escreva("============================================")
    escreva("")
    escreva("OPERADOR MÓDULO (%) - EXEMPLOS:")
    escreva("10 % 3 =", 10 % 3, " (resto 1)")
    escreva("15 % 4 =", 15 % 4, " (resto 3)")
    escreva("20 % 5 =", 20 % 5, " (resto 0 - divisível!)")
    escreva("7 % 2 =", 7 % 2, " (resto 1 - ímpar!)")
fim
