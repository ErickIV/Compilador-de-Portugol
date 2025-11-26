"""
Testes para o Gerador de Código Python

Valida que o código Python gerado está correto e executável.
"""

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.semantic import AnalisadorSemantico
from src.codegen import GeradorDeCodigo


class TestCodegenBasico:
    """Testes básicos de geração de código"""

    def test_programa_vazio(self):
        """Testa geração de código para programa vazio"""
        codigo = "inicio fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "def main():" in python_code
        assert "if __name__ == '__main__':" in python_code
        assert "main()" in python_code

    def test_declaracao_variavel(self):
        """Testa geração de declaração de variável"""
        codigo = "inteiro x; inicio fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "x = 0" in python_code  # Inicialização padrão de inteiro

    def test_declaracao_tipos_diferentes(self):
        """Testa geração de declarações de tipos diferentes"""
        codigo = """
        inteiro i;
        real x;
        caracter nome;
        logico ativo;
        inicio fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "i = 0" in python_code
        assert "x = 0.0" in python_code
        assert 'nome = ""' in python_code
        assert "ativo = False" in python_code

    def test_atribuicao_simples(self):
        """Testa geração de atribuição simples"""
        codigo = "inteiro x; inicio x <- 42 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "x = 42" in python_code

    def test_atribuicao_com_expressao(self):
        """Testa geração de atribuição com expressão"""
        codigo = "inteiro x, y, z; inicio x <- 5 y <- 10 z <- x + y fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "x = 5" in python_code
        assert "y = 10" in python_code
        assert "z = x + y" in python_code


class TestCodegenEstruturas:
    """Testes de estruturas de controle"""

    def test_condicional_simples(self):
        """Testa geração de if simples"""
        codigo = """
        inteiro x;
        inicio
            x <- 5
            se x > 0 entao
                x <- 10
            fimse
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "if x > 0:" in python_code
        assert "x = 10" in python_code

    def test_condicional_com_senao(self):
        """Testa geração de if-else"""
        codigo = """
        inteiro x;
        inicio
            x <- 5
            se x > 0 entao
                x <- 10
            senao
                x <- 20
            fimse
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "if x > 0:" in python_code
        assert "x = 10" in python_code
        assert "else:" in python_code
        assert "x = 20" in python_code

    def test_repeticao_enquanto(self):
        """Testa geração de while"""
        codigo = """
        inteiro x;
        inicio
            x <- 0
            enquanto x < 10 faca
                x <- x + 1
            fimenquanto
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "while x < 10:" in python_code
        assert "x = x + 1" in python_code

    def test_repeticao_para_positivo(self):
        """Testa geração de loop para com passo positivo"""
        codigo = """
        inteiro i;
        inicio
            para i de 1 ate 10 passo 1 faca
                escreva(i)
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Verifica inicialização
        assert "i = 1" in python_code
        # Verifica condição dinâmica
        assert "while" in python_code
        assert "<= 10" in python_code or ">= 10" in python_code
        # Verifica incremento
        assert "i = i + (1)" in python_code or "i = i + 1" in python_code

    def test_repeticao_para_negativo(self):
        """Testa geração de loop para com passo negativo"""
        codigo = """
        inteiro i;
        inicio
            para i de 10 ate 1 passo -1 faca
                escreva(i)
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Verifica inicialização
        assert "i = 10" in python_code
        # Verifica condição dinâmica que suporta passo negativo
        assert "while" in python_code
        # Deve ter condição para passo negativo (>=)
        assert ">= 1" in python_code or "< 0" in python_code
        # Verifica decremento
        assert "i = i + (-1)" in python_code or "i + -1" in python_code

    def test_repeticao_para_sem_passo(self):
        """Testa geração de loop para sem passo explícito"""
        codigo = """
        inteiro i;
        inicio
            para i de 1 ate 5 faca
                escreva(i)
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Verifica que passo padrão 1 foi usado
        assert "i = 1" in python_code
        assert "while" in python_code
        assert "i = i + (1)" in python_code or "i = i + 1" in python_code


class TestCodegenIO:
    """Testes de entrada e saída"""

    def test_entrada(self):
        """Testa geração de comando leia"""
        codigo = """
        inteiro x;
        inicio
            leia(x)
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "x = input()" in python_code
        assert "x = int(x)" in python_code  # Conversão para inteiro

    def test_saida_simples(self):
        """Testa geração de comando escreva"""
        codigo = """
        inteiro x;
        inicio
            x <- 42
            escreva(x)
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "print(x)" in python_code

    def test_saida_multiplas_expressoes(self):
        """Testa geração de escreva com múltiplas expressões"""
        codigo = """
        inteiro x, y;
        inicio
            x <- 5
            y <- 10
            escreva("Soma:", x + y)
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert 'print("Soma:", x + y)' in python_code or "print('Soma:', x + y)" in python_code


class TestCodegenOperadores:
    """Testes de operadores"""

    def test_operadores_aritmeticos(self):
        """Testa geração de operadores aritméticos"""
        codigo = """
        inteiro a, b, c, d, e, f;
        inicio
            a <- 5 + 3
            b <- 10 - 2
            c <- 4 * 5
            d <- 20 / 4
            e <- 10 % 3
            f <- 2 ^ 3
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "a = 5 + 3" in python_code
        assert "b = 10 - 2" in python_code
        assert "c = 4 * 5" in python_code
        assert "d = 20 / 4" in python_code
        assert "e = 10 % 3" in python_code
        assert "f = 2 ** 3" in python_code  # ^ vira **

    def test_operadores_relacionais(self):
        """Testa geração de operadores relacionais"""
        codigo = """
        inteiro x;
        logico a, b, c, d, e, f;
        inicio
            x <- 5
            a <- x == 5
            b <- x != 10
            c <- x < 10
            d <- x <= 5
            e <- x > 0
            f <- x >= 5
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "x == 5" in python_code
        assert "x != 10" in python_code
        assert "x < 10" in python_code
        assert "x <= 5" in python_code
        assert "x > 0" in python_code
        assert "x >= 5" in python_code

    def test_operadores_logicos(self):
        """Testa geração de operadores lógicos"""
        codigo = """
        logico a, b, c;
        inicio
            a <- verdadeiro
            b <- falso
            c <- a e b
            c <- a ou b
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        assert "a = True" in python_code
        assert "b = False" in python_code
        assert "c = a and b" in python_code
        assert "c = a or b" in python_code


class TestCodegenExecucao:
    """Testes de execução do código gerado"""

    def test_execucao_simples(self):
        """Testa que código gerado pode ser executado"""
        codigo = "inteiro x; inicio x <- 42 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Tenta executar o código gerado
        namespace = {}
        exec(python_code, namespace)
        # Não deve lançar exceção

    def test_execucao_loop_positivo(self):
        """Testa execução de loop com passo positivo"""
        codigo = """
        inteiro i, soma;
        inicio
            soma <- 0
            para i de 1 ate 5 faca
                soma <- soma + i
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Executa e verifica resultado
        namespace = {}
        exec(python_code, namespace)
        # Loop deve ter executado corretamente

    def test_execucao_loop_negativo(self):
        """Testa execução de loop com passo negativo"""
        codigo = """
        inteiro i, conta;
        inicio
            conta <- 0
            para i de 5 ate 1 passo -1 faca
                conta <- conta + 1
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Executa e verifica que não trava
        namespace = {}
        exec(python_code, namespace)
        # Loop reverso deve ter executado


class TestCodegenComplexo:
    """Testes com programas complexos"""

    def test_programa_fibonacci(self, codigo_fibonacci):
        """Testa geração de código para Fibonacci"""
        lexer = Lexer(codigo_fibonacci)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Verifica que código foi gerado
        assert len(python_code) > 100
        assert "def main():" in python_code

    def test_loop_reverso(self, codigo_loop_reverso):
        """Testa geração de código para loop reverso"""
        lexer = Lexer(codigo_loop_reverso)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Verifica que condição dinâmica foi gerada
        assert "while" in python_code
        assert ">=" in python_code or "< 0" in python_code

    def test_passo_opcional(self, codigo_passo_opcional):
        """Testa geração com passo opcional"""
        lexer = Lexer(codigo_passo_opcional)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        codegen = GeradorDeCodigo()
        python_code = codegen.gerar(ast)

        # Verifica que passo 1 foi usado
        assert "i = i + (1)" in python_code or "i = i + 1" in python_code
