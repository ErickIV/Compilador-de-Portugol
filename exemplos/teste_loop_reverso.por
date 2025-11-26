// Teste de Loop Reverso com Passo Negativo
// Este programa demonstra o uso do loop 'para' com passo negativo
// que agora funciona corretamente após as melhorias no compilador

inteiro i;

inicio
    escreva("=== Teste de Loop Reverso ===")
    escreva("Contagem regressiva de 10 até 1:")
    escreva("")

    // Loop com passo negativo
    para i de 10 ate 1 passo -1 faca
        escreva("Contagem:", i)
    fimpara

    escreva("")
    escreva("Contagem regressiva finalizada!")
    escreva("")

    escreva("=== Teste de Passo Opcional ===")
    escreva("Contagem de 1 até 5 (sem passo explícito):")
    escreva("")

    // Loop sem passo explícito (usa padrão 1)
    para i de 1 ate 5 faca
        escreva("Número:", i)
    fimpara

    escreva("")
    escreva("=== Teste de Passo 2 ===")
    escreva("Números pares de 0 até 10:")
    escreva("")

    // Loop com passo 2
    para i de 0 ate 10 passo 2 faca
        escreva(i)
    fimpara

    escreva("")
    escreva("Todos os testes concluídos!")
fim
