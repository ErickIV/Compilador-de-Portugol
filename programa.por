// Programa para testar edge cases e robustez do compilador
// Testa limites, casos especiais e diferentes construções

// Declarações de variáveis (ANTES do inicio)
inteiro idade, ano;
real altura, peso, imc;
caracter categoria;
logico eh_adulto, eh_obeso;

// Teste de números extremos e operações
inteiro zero, negativo, muito_grande;
real pi_preciso, numero_pequeno;

inicio

    zero <- 0
    negativo <- 0 - 100
    muito_grande <- 999999
    pi_preciso <- 3.141592653589793
    numero_pequeno <- 0.000001

    escreva("=== TESTE DE ROBUSTEZ ===")
    
    // Teste de divisão por zero (cuidado!)
    escreva("Testando operações matemáticas:")
    escreva("Zero + 5 = ", zero + 5)
    escreva("Negativo * 2 = ", negativo * 2)
    escreva("Pi preciso = ", pi_preciso)
    
    // Teste de condições complexas
    escreva("Digite sua idade: ")
    leia(idade)
    
    escreva("Digite sua altura (em metros): ")
    leia(altura)
    
    escreva("Digite seu peso (em kg): ")
    leia(peso)

    // Validações aninhadas complexas
    se (idade <= 0) entao
        escreva("Idade inválida!")
    senao
        se (altura <= 0.5) entao
            escreva("Altura muito baixa!")
        senao
            se (peso <= 0) entao
                escreva("Peso inválido!")
            senao
                // Cálculos válidos
                eh_adulto <- idade >= 18
                imc <- peso / (altura * altura)
                
                escreva("=== RESULTADOS ===")
                escreva("Idade: ", idade, " anos")
                escreva("Altura: ", altura, " metros")
                escreva("Peso: ", peso, " kg")
                escreva("IMC: ", imc)
                
                // Classificação de idade
                se (eh_adulto) entao
                    escreva("Status: ADULTO")
                    
                    se (idade >= 60) entao
                        escreva("Categoria: IDOSO")
                    senao
                        se (idade >= 30) entao
                            escreva("Categoria: ADULTO MADURO")
                        senao
                            escreva("Categoria: JOVEM ADULTO")
                        fimse
                    fimse
                senao
                    escreva("Status: MENOR DE IDADE")
                    
                    se (idade >= 13) entao
                        escreva("Categoria: ADOLESCENTE")
                    senao
                        escreva("Categoria: CRIANÇA")
                    fimse
                fimse
                
                // Classificação IMC
                se (imc < 18.5) entao
                    escreva("IMC: ABAIXO DO PESO")
                senao
                    se (imc < 25.0) entao
                        escreva("IMC: PESO NORMAL")
                    senao
                        se (imc < 30.0) entao
                            escreva("IMC: SOBREPESO")
                        senao
                            escreva("IMC: OBESIDADE")
                            eh_obeso <- verdadeiro
                        fimse
                    fimse
                fimse
                
                // Recomendações baseadas em múltiplas condições
                se (eh_adulto == verdadeiro e eh_obeso == verdadeiro) entao
                    escreva("Recomendação: Consulte um médico urgentemente!")
                senao
                    se (idade > 50 e imc > 27.0) entao
                        escreva("Recomendação: Cuidado com a saúde!")
                    senao
                        se (idade < 18 e imc < 18.5) entao
                            escreva("Recomendação: Consulte um pediatra")
                        senao
                            escreva("Recomendação: Continue cuidando da saúde!")
                        fimse
                    fimse
                fimse
            fimse
        fimse
    fimse
    
    // Teste de loop simples
    escreva("=== TESTE DE CONTAGEM ===")
    ano <- 2024
    enquanto (ano <= 2030) faca
        escreva("Processando ano: ", ano)
        ano <- ano + 1
    fimenquanto
    
    escreva("Teste de robustez concluído!")
fim
