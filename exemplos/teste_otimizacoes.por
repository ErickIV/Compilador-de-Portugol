/* Teste de Otimizações do Compilador Portugol */

inteiro a, b, c, resultado;
real x, y;

inicio
    /* Constant Folding: 5 + 3 calculado em compilação */
    a <- 5 + 3
    
    /* Operação com constantes */
    b <- 10 * 2 + 5
    
    /* Simplificação: x + 0 = x */
    resultado <- a + 0
    
    /* Simplificação: x * 1 = x */
    resultado <- b * 1
    
    /* Simplificação: x * 0 = 0 */
    c <- resultado * 0
    
    /* Simplificação: x - 0 = x */
    resultado <- a - 0
    
    /* Constant Propagation */
    x <- 3.14
    y <- x + 1.0
    
    /* Exibir resultados */
    escreva("Resultados após otimizações:")
    escreva("a = ", a)
    escreva("b = ", b)
    escreva("c = ", c)
    escreva("y = ", y)
    
    /* Expressão complexa otimizada */
    resultado <- (5 + 3) * (10 - 2)
    escreva("Expressão complexa: ", resultado)
fim
