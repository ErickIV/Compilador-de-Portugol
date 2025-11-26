// Teste de Strings com Caracteres Escapados
// Este programa demonstra o tratamento correto de escape em strings
// implementado no compilador

caracter texto, caminho;

inicio
    escreva("=== Teste de Strings com Escape ===")
    escreva("")

    // Teste 1: Aspas escapadas
    escreva("Teste 1: Aspas Escapadas")
    texto <- "Ele disse: \"Olá, mundo!\""
    escreva(texto)
    escreva("")

    // Teste 2: Barra invertida
    escreva("Teste 2: Caminho de Arquivo")
    caminho <- "C:\\Users\\Documents\\arquivo.txt"
    escreva("Caminho:", caminho)
    escreva("")

    // Teste 3: Múltiplas aspas
    escreva("Teste 3: Múltiplas Aspas")
    texto <- "O livro \"1984\" de \"George Orwell\""
    escreva(texto)
    escreva("")

    // Teste 4: Newline (representação)
    escreva("Teste 4: Quebra de Linha")
    texto <- "Primeira linha\\nSegunda linha"
    escreva("Texto com \\n:", texto)
    escreva("")

    escreva("=== Todos os testes de escape concluídos! ===")
fim
