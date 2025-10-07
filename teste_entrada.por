// Teste simples de entrada e conversões
inteiro idade;
real altura;
caracter nome;
logico ativo;

inicio
    escreva("Digite seu nome:")
    leia(nome)
    
    escreva("Digite sua idade:")
    leia(idade)
    
    escreva("Digite sua altura:")
    leia(altura)
    
    escreva("Está ativo? (true/false):")
    leia(ativo)
    
    escreva("=== DADOS DIGITADOS ===")
    escreva("Nome:", nome)
    escreva("Idade:", idade)
    escreva("Altura:", altura)
    escreva("Ativo:", ativo)
    
    se idade >= 18 entao
        escreva("Você é maior de idade!")
    senao
        escreva("Você é menor de idade!")
    fimse
fim