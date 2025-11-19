// ============================================================================
// PROGRAMA: Calculadora de IMC (Índice de Massa Corporal)
// DESCRIÇÃO: Demonstra uso de variáveis, entrada/saída, cálculos e decisões
// FUNCIONALIDADES TESTADAS:
//   - Declaração de variáveis (inteiro, real, caracter, logico)
//   - Entrada de dados (leia)
//   - Operações aritméticas (+, -, *, /)
//   - Operadores relacionais (<, <=, >, >=, ==, !=)
//   - Estruturas condicionais aninhadas (se-entao-senao)
//   - Operadores lógicos (e, ou)
//   - Saída formatada (escreva)
// ============================================================================

inteiro idade;
real altura, peso, imc;
caracter nome, categoria;
logico eh_adulto, eh_saudavel;

inicio
    escreva("============================================")
    escreva("   CALCULADORA DE IMC - ÍNDICE DE MASSA    ")
    escreva("           CORPORAL E SAÚDE                ")
    escreva("============================================")
    escreva("")
    
    // Entrada de dados do usuário
    escreva("Digite seu nome: ")
    leia(nome)
    
    escreva("Digite sua idade: ")
    leia(idade)
    
    escreva("Digite sua altura em metros (ex: 1.75): ")
    leia(altura)
    
    escreva("Digite seu peso em kg (ex: 70.5): ")
    leia(peso)
    
    escreva("")
    escreva("--------------------------------------------")
    escreva("              PROCESSANDO...                ")
    escreva("--------------------------------------------")
    escreva("")
    
    // Validações de entrada
    se idade <= 0 ou idade > 120 entao
        escreva("ERRO: Idade inválida!")
    senao
        se altura <= 0.0 ou altura > 3.0 entao
            escreva("ERRO: Altura inválida!")
        senao
            se peso <= 0.0 ou peso > 500.0 entao
                escreva("ERRO: Peso inválido!")
            senao
                // Cálculo do IMC (IMC = peso / altura²)
                imc <- peso / (altura * altura)
                
                // Determinação de status
                eh_adulto <- idade >= 18
                
                // Resultados
                escreva("============================================")
                escreva("              RESULTADOS                    ")
                escreva("============================================")
                escreva("Nome: ", nome)
                escreva("Idade: ", idade, " anos")
                escreva("Altura: ", altura, " metros")
                escreva("Peso: ", peso, " kg")
                escreva("IMC calculado: ", imc)
                escreva("")
                
                // Classificação etária
                escreva("--- CLASSIFICAÇÃO ETÁRIA ---")
                se eh_adulto entao
                    escreva("Status: ADULTO")
                    
                    se idade >= 60 entao
                        escreva("Faixa: IDOSO (60+ anos)")
                    senao
                        se idade >= 30 entao
                            escreva("Faixa: ADULTO MADURO (30-59 anos)")
                        senao
                            escreva("Faixa: JOVEM ADULTO (18-29 anos)")
                        fimse
                    fimse
                senao
                    escreva("Status: MENOR DE IDADE")
                    
                    se idade >= 13 entao
                        escreva("Faixa: ADOLESCENTE (13-17 anos)")
                    senao
                        escreva("Faixa: CRIANÇA (0-12 anos)")
                    fimse
                fimse
                
                escreva("")
                escreva("--- CLASSIFICAÇÃO DO IMC ---")
                
                // Classificação do IMC segundo OMS
                se imc < 18.5 entao
                    categoria <- "ABAIXO DO PESO"
                    escreva("Categoria: ", categoria)
                    escreva("Recomendação: Consulte um nutricionista")
                    eh_saudavel <- falso
                senao
                    se imc < 25.0 entao
                        categoria <- "PESO NORMAL"
                        escreva("Categoria: ", categoria)
                        escreva("Recomendação: Mantenha seus hábitos saudáveis!")
                        eh_saudavel <- verdadeiro
                    senao
                        se imc < 30.0 entao
                            categoria <- "SOBREPESO"
                            escreva("Categoria: ", categoria)
                            escreva("Recomendação: Atenção à dieta e exercícios")
                            eh_saudavel <- falso
                        senao
                            se imc < 35.0 entao
                                categoria <- "OBESIDADE GRAU I"
                                escreva("Categoria: ", categoria)
                                escreva("Recomendação: Consulte um médico urgentemente")
                                eh_saudavel <- falso
                            senao
                                se imc < 40.0 entao
                                    categoria <- "OBESIDADE GRAU II"
                                    escreva("Categoria: ", categoria)
                                    escreva("Recomendação: Acompanhamento médico necessário!")
                                    eh_saudavel <- falso
                                senao
                                    categoria <- "OBESIDADE GRAU III"
                                    escreva("Categoria: ", categoria)
                                    escreva("Recomendação: Procure um médico imediatamente!")
                                    eh_saudavel <- falso
                                fimse
                            fimse
                        fimse
                    fimse
                fimse
                
                escreva("")
                escreva("--- ANÁLISE FINAL ---")
                
                // Recomendações personalizadas
                se eh_adulto e eh_saudavel entao
                    escreva("Parabéns! Você está com peso saudável.")
                    escreva("Continue mantendo uma vida ativa!")
                senao
                    se eh_adulto e imc >= 30.0 entao
                        escreva("ATENÇÃO: Obesidade detectada!")
                        escreva("Consulte profissionais de saúde.")
                    senao
                        se idade < 18 e imc < 18.5 entao
                            escreva("Menor com peso baixo.")
                            escreva("Consulte um pediatra para orientação.")
                        senao
                            escreva("Procure orientação profissional")
                            escreva("para melhorar sua saúde.")
                        fimse
                    fimse
                fimse
                
                escreva("")
                escreva("============================================")
                escreva("     Obrigado por usar nossa calculadora!  ")
                escreva("============================================")
            fimse
        fimse
    fimse
fim
