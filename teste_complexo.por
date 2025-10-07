// Programa mais complexo - Sistema de Notas Escolares
// Demonstra: loops aninhados, validações, cálculos complexos

// Declarações de variáveis (ANTES do inicio)
inteiro num_alunos, num_provas, i, j, nota, soma_total, soma_aluno;
real media_aluno, media_geral, maior_media, menor_media;
inteiro aprovados, reprovados;
logico primeira_iteracao;

inicio
    // Configuração inicial
    aprovados <- 0
    reprovados <- 0
    soma_total <- 0
    primeira_iteracao <- verdadeiro
    maior_media <- 0.0
    menor_media <- 10.0

    escreva("=== SISTEMA DE NOTAS ESCOLARES ===")
    escreva("Quantos alunos? ")
    leia(num_alunos)
    
    escreva("Quantas provas por aluno? ")
    leia(num_provas)

    // Validação de entrada
    se num_alunos <= 0 entao
        escreva("Erro: Número de alunos deve ser positivo!")
    senao
        se num_provas <= 0 entao
            escreva("Erro: Número de provas deve ser positivo!")
        senao
            // Processamento principal
            i <- 1
            enquanto i <= num_alunos faca
                escreva("--- Aluno ", i, " ---")
                soma_aluno <- 0
                
                // Lê as notas do aluno
                j <- 1
                enquanto j <= num_provas faca
                    escreva("Nota da prova ", j, ": ")
                    leia(nota)
                    
                    // Validação da nota
                    se nota < 0 entao
                        escreva("Nota inválida! Usando 0.")
                        nota <- 0
                    senao
                        se nota > 10 entao
                            escreva("Nota inválida! Usando 10.")
                            nota <- 10
                        fimse
                    fimse
                    
                    soma_aluno <- soma_aluno + nota
                    j <- j + 1
                fimenquanto
                
                // Calcula média do aluno
                media_aluno <- soma_aluno / num_provas
                escreva("Média do aluno ", i, ": ", media_aluno)
                
                // Verifica aprovação
                se media_aluno >= 7.0 entao
                    escreva("Status: APROVADO")
                    aprovados <- aprovados + 1
                senao
                    se media_aluno >= 5.0 entao
                        escreva("Status: RECUPERAÇÃO")
                    senao
                        escreva("Status: REPROVADO")
                        reprovados <- reprovados + 1
                    fimse
                fimse
                
                // Atualiza estatísticas
                se primeira_iteracao entao
                    maior_media <- media_aluno
                    menor_media <- media_aluno
                    primeira_iteracao <- falso
                senao
                    se media_aluno > maior_media entao
                        maior_media <- media_aluno
                    fimse
                    se media_aluno < menor_media entao
                        menor_media <- media_aluno
                    fimse
                fimse
                
                soma_total <- soma_total + media_aluno
                i <- i + 1
            fimenquanto
            
            // Relatório final
            escreva("=== RELATÓRIO FINAL ===")
            media_geral <- soma_total / num_alunos
            escreva("Média geral da turma: ", media_geral)
            escreva("Maior média: ", maior_media)
            escreva("Menor média: ", menor_media)
            escreva("Alunos aprovados: ", aprovados)
            escreva("Alunos reprovados: ", reprovados)
            
            // Análise da turma
            se media_geral >= 8.0 entao
                escreva("Análise: Turma EXCELENTE!")
            senao
                se media_geral >= 7.0 entao
                    escreva("Análise: Turma BOA!")
                senao
                    se media_geral >= 6.0 entao
                        escreva("Análise: Turma REGULAR")
                    senao
                        escreva("Análise: Turma precisa de ATENÇÃO")
                    fimse
                fimse
            fimse
        fimse
    fimse
    
    escreva("Programa finalizado.")
fim