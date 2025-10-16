// ============================================================================
// PROGRAMA: Demonstração Completa de Funcionalidades
// DESCRIÇÃO: Programa para teste rápido e demonstração em sala
// FUNCIONALIDADES TESTADAS:
//   - Todos os tipos de dados (inteiro, real, caracter, logico)
//   - Todas as operações aritméticas (+, -, *, /)
//   - Todos os operadores relacionais (<, <=, >, >=, ==, !=)
//   - Operadores lógicos (e, ou)
//   - Condicionais simples e aninhadas
//   - Loops com contadores
//   - Expressões complexas
//   - Comentários inline e de bloco
// ============================================================================

inteiro contador, soma, resultado;
real pi, raio, area, perimetro;
caracter mensagem;
logico condicao_verdadeira, condicao_falsa;

inicio
    escreva("============================================")
    escreva("  DEMONSTRAÇÃO COMPLETA DO COMPILADOR      ")
    escreva("          PORTUGOL -> PYTHON               ")
    escreva("============================================")
    escreva("")
    
    // ========================================
    // SEÇÃO 1: TIPOS DE DADOS E ATRIBUIÇÕES
    // ========================================
    escreva("--- 1. TIPOS DE DADOS ---")
    
    contador <- 42
    pi <- 3.14159
    mensagem <- "Olá, Portugol!"
    condicao_verdadeira <- verdadeiro
    condicao_falsa <- falso
    
    escreva("Inteiro:", contador)
    escreva("Real:", pi)
    escreva("Caracter:", mensagem)
    escreva("Lógico verdadeiro:", condicao_verdadeira)
    escreva("Lógico falso:", condicao_falsa)
    escreva("")
    
    // ========================================
    // SEÇÃO 2: OPERAÇÕES ARITMÉTICAS
    // ========================================
    escreva("--- 2. OPERAÇÕES ARITMÉTICAS ---")
    
    soma <- 10 + 5
    escreva("Adição: 10 + 5 =", soma)
    
    resultado <- 20 - 8
    escreva("Subtração: 20 - 8 =", resultado)
    
    resultado <- 6 * 7
    escreva("Multiplicação: 6 * 7 =", resultado)
    
    raio <- 15.0 / 3.0
    escreva("Divisão: 15.0 / 3.0 =", raio)
    
    resultado <- 5 + 3 * 2
    escreva("Precedência: 5 + 3 * 2 =", resultado)
    escreva("")
    
    // ========================================
    // SEÇÃO 3: OPERADORES RELACIONAIS
    // ========================================
    escreva("--- 3. OPERADORES RELACIONAIS ---")
    
    escreva("10 > 5 =", 10 > 5)
    escreva("10 < 5 =", 10 < 5)
    escreva("10 >= 10 =", 10 >= 10)
    escreva("5 <= 3 =", 5 <= 3)
    escreva("42 == 42 =", 42 == 42)
    escreva("42 != 40 =", 42 != 40)
    escreva("")
    
    // ========================================
    // SEÇÃO 4: OPERADORES LÓGICOS
    // ========================================
    escreva("--- 4. OPERADORES LÓGICOS ---")
    
    escreva("verdadeiro E verdadeiro =", verdadeiro e verdadeiro)
    escreva("verdadeiro E falso =", verdadeiro e falso)
    escreva("falso OU verdadeiro =", falso ou verdadeiro)
    escreva("falso OU falso =", falso ou falso)
    escreva("(10 > 5) E (20 < 30) =", 10 > 5 e 20 < 30)
    escreva("")
    
    // ========================================
    // SEÇÃO 5: ESTRUTURAS CONDICIONAIS
    // ========================================
    escreva("--- 5. ESTRUTURAS CONDICIONAIS ---")
    
    contador <- 15
    se contador > 10 entao
        escreva("Condicional simples: contador > 10 ✓")
    fimse
    
    se contador < 10 entao
        escreva("Este texto não aparece")
    senao
        escreva("Condicional com senao: contador >= 10 ✓")
    fimse
    
    // Condicional aninhada
    se contador >= 10 entao
        se contador <= 20 entao
            escreva("Condicional aninhada: 10 <= contador <= 20 ✓")
        fimse
    fimse
    escreva("")
    
    // ========================================
    // SEÇÃO 6: ESTRUTURAS DE REPETIÇÃO
    // ========================================
    escreva("--- 6. ESTRUTURAS DE REPETIÇÃO ---")
    
    escreva("Contagem de 1 a 5:")
    contador <- 1
    enquanto contador <= 5 faca
        escreva("  Contador:", contador)
        contador <- contador + 1
    fimenquanto
    
    escreva("Soma dos números de 1 a 10:")
    soma <- 0
    contador <- 1
    enquanto contador <= 10 faca
        soma <- soma + contador
        contador <- contador + 1
    fimenquanto
    escreva("  Resultado:", soma)
    escreva("")
    
    // ========================================
    // SEÇÃO 7: CÁLCULOS MATEMÁTICOS
    // ========================================
    escreva("--- 7. CÁLCULOS MATEMÁTICOS ---")
    
    pi <- 3.14159
    raio <- 5.0
    
    area <- pi * raio * raio
    perimetro <- 2.0 * pi * raio
    
    escreva("Círculo com raio =", raio)
    escreva("Área =", area)
    escreva("Perímetro =", perimetro)
    escreva("")
    
    // ========================================
    // SEÇÃO 8: TABUADA
    // ========================================
    escreva("--- 8. TABUADA DO 7 ---")
    
    contador <- 1
    enquanto contador <= 10 faca
        resultado <- 7 * contador
        escreva("7 x", contador, "=", resultado)
        contador <- contador + 1
    fimenquanto
    escreva("")
    
    // ========================================
    // SEÇÃO 9: CLASSIFICAÇÃO DE NÚMEROS
    // ========================================
    escreva("--- 9. CLASSIFICAÇÃO DE NÚMEROS ---")
    
    contador <- 0 - 5
    escreva("Número:", contador)
    
    se contador < 0 entao
        escreva("  Classificação: NEGATIVO")
    senao
        se contador == 0 entao
            escreva("  Classificação: ZERO")
        senao
            escreva("  Classificação: POSITIVO")
        fimse
    fimse
    
    se contador < 0 entao
        resultado <- 0 - contador
    senao
        resultado <- contador
    fimse
    escreva("  Valor absoluto:", resultado)
    escreva("")
    
    // ========================================
    // SEÇÃO 10: ANÁLISE DE PAR/ÍMPAR
    // ========================================
    escreva("--- 10. ANÁLISE PAR/ÍMPAR (1-10) ---")
    
    contador <- 1
    enquanto contador <= 10 faca
        // Simulação de módulo usando divisão
        resultado <- contador / 2
        resultado <- resultado * 2
        
        se resultado == contador entao
            escreva("  ", contador, "é PAR")
        senao
            escreva("  ", contador, "é ÍMPAR")
        fimse
        
        contador <- contador + 1
    fimenquanto
    escreva("")
    
    // ========================================
    // FINALIZAÇÃO
    // ========================================
    escreva("============================================")
    escreva("  TODAS AS FUNCIONALIDADES TESTADAS!       ")
    escreva("============================================")
    escreva("")
    escreva("Compilador Portugol funcionando perfeitamente!")
    escreva("✓ Análise Léxica")
    escreva("✓ Análise Sintática")
    escreva("✓ Análise Semântica")
    escreva("✓ Geração de Código Python")
    escreva("")
    escreva("Projeto desenvolvido como trabalho acadêmico")
    escreva("Disciplina: Compiladores")
fim
