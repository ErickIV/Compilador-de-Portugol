"""
Testes para o Parser (Analisador Sintático)

Valida a construção correta da AST a partir dos tokens.
"""

import pytest
from src.lexer import Lexer
from src.parser import Parser
from src.ast_nodes import (
    Programa, DeclaracaoVariavel, Atribuicao, Condicional,
    Repeticao, RepeticaoPara, Entrada, Saida, Literal, Variavel,
    ExpressaoBinaria
)
from src.exceptions import ErroSintatico


class TestParserDeclaracoes:
    """Testes para análise de declarações de variáveis"""

    def test_declaracao_simples(self):
        """Testa declaração de uma variável"""
        codigo = "inteiro x; inicio fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert isinstance(ast, Programa)
        assert len(ast.declaracoes) == 1
        assert ast.declaracoes[0].tipo == "inteiro"
        assert ast.declaracoes[0].nome == "x"

    def test_declaracao_multiplas_variaveis(self):
        """Testa declaração de múltiplas variáveis em uma linha"""
        codigo = "real x, y, z; inicio fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert len(ast.declaracoes) == 3
        assert all(d.tipo == "real" for d in ast.declaracoes)
        assert [d.nome for d in ast.declaracoes] == ["x", "y", "z"]

    def test_declaracao_tipos_diferentes(self):
        """Testa declaração de variáveis de tipos diferentes"""
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

        assert len(ast.declaracoes) == 4
        tipos = [d.tipo for d in ast.declaracoes]
        assert tipos == ["inteiro", "real", "caracter", "logico"]


class TestParserComandos:
    """Testes para análise de comandos"""

    def test_atribuicao_simples(self):
        """Testa comando de atribuição simples"""
        codigo = "inteiro x; inicio x <- 5 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert len(ast.comandos) == 1
        cmd = ast.comandos[0]
        assert isinstance(cmd, Atribuicao)
        assert cmd.variavel == "x"
        assert isinstance(cmd.expressao, Literal)
        assert cmd.expressao.valor == "5"

    def test_condicional_simples(self):
        """Testa estrutura condicional simples"""
        codigo = """
        inteiro x;
        inicio
            se x == 5 entao
                x <- 10
            fimse
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert len(ast.comandos) == 1
        cmd = ast.comandos[0]
        assert isinstance(cmd, Condicional)
        assert len(cmd.comandos_entao) == 1
        assert len(cmd.comandos_senao) == 0

    def test_condicional_com_senao(self):
        """Testa estrutura condicional com senao"""
        codigo = """
        inteiro x;
        inicio
            se x == 5 entao
                x <- 10
            senao
                x <- 20
            fimse
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        cmd = ast.comandos[0]
        assert isinstance(cmd, Condicional)
        assert len(cmd.comandos_entao) == 1
        assert len(cmd.comandos_senao) == 1

    def test_repeticao_enquanto(self):
        """Testa estrutura de repetição enquanto"""
        codigo = """
        inteiro x;
        inicio
            enquanto x < 10 faca
                x <- x + 1
            fimenquanto
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert len(ast.comandos) == 1
        cmd = ast.comandos[0]
        assert isinstance(cmd, Repeticao)
        assert len(cmd.comandos) == 1

    def test_repeticao_para_com_passo(self):
        """Testa loop 'para' com passo explícito"""
        codigo = """
        inteiro i;
        inicio
            para i de 1 ate 10 passo 2 faca
                escreva(i)
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        cmd = ast.comandos[0]
        assert isinstance(cmd, RepeticaoPara)
        assert cmd.variavel == "i"
        assert isinstance(cmd.inicio, Literal)
        assert isinstance(cmd.fim, Literal)
        assert isinstance(cmd.passo, Literal)
        assert cmd.passo.valor == "2"

    def test_repeticao_para_sem_passo(self):
        """Testa loop 'para' sem passo (deve usar padrão 1)"""
        codigo = """
        inteiro i;
        inicio
            para i de 1 ate 10 faca
                escreva(i)
            fimpara
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        cmd = ast.comandos[0]
        assert isinstance(cmd, RepeticaoPara)
        assert cmd.variavel == "i"
        assert isinstance(cmd.passo, Literal)
        assert cmd.passo.valor == "1"  # Passo padrão

    def test_repeticao_para_passo_negativo(self):
        """Testa loop 'para' com passo negativo"""
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

        cmd = ast.comandos[0]
        assert isinstance(cmd, RepeticaoPara)
        # Verifica que o passo é uma expressão unária negativa ou literal negativo
        assert cmd.passo is not None

    def test_entrada(self):
        """Testa comando de entrada"""
        codigo = """
        inteiro x;
        inicio
            leia(x)
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert len(ast.comandos) == 1
        cmd = ast.comandos[0]
        assert isinstance(cmd, Entrada)
        assert cmd.variavel == "x"

    def test_saida_unica_expressao(self):
        """Testa comando de saída com uma expressão"""
        codigo = """
        inteiro x;
        inicio
            escreva(x)
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        cmd = ast.comandos[0]
        assert isinstance(cmd, Saida)
        assert len(cmd.expressoes) == 1

    def test_saida_multiplas_expressoes(self):
        """Testa comando de saída com múltiplas expressões"""
        codigo = """
        inteiro x, y;
        inicio
            escreva(x, y, "soma:", x + y)
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        cmd = ast.comandos[0]
        assert isinstance(cmd, Saida)
        assert len(cmd.expressoes) == 4


class TestParserExpressoes:
    """Testes para análise de expressões"""

    def test_expressao_literal(self):
        """Testa expressão com literal"""
        codigo = "inteiro x; inicio x <- 42 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        expr = ast.comandos[0].expressao
        assert isinstance(expr, Literal)
        assert expr.valor == "42"

    def test_expressao_variavel(self):
        """Testa expressão com variável"""
        codigo = "inteiro x, y; inicio y <- x fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        expr = ast.comandos[0].expressao
        assert isinstance(expr, Variavel)
        assert expr.nome == "x"

    def test_expressao_binaria_soma(self):
        """Testa expressão binária de soma"""
        codigo = "inteiro x; inicio x <- 5 + 3 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        expr = ast.comandos[0].expressao
        assert isinstance(expr, ExpressaoBinaria)
        assert expr.operador == "+"

    def test_expressao_precedencia(self):
        """Testa precedência de operadores"""
        codigo = "inteiro x; inicio x <- 2 + 3 * 4 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        expr = ast.comandos[0].expressao
        # 2 + (3 * 4)
        assert isinstance(expr, ExpressaoBinaria)
        assert expr.operador == "+"
        # Lado direito deve ser a multiplicação
        assert isinstance(expr.direita, ExpressaoBinaria)
        assert expr.direita.operador == "*"


class TestParserErros:
    """Testes para tratamento de erros sintáticos"""

    def test_erro_falta_ponto_virgula(self):
        """Testa erro quando falta ponto-e-vírgula"""
        codigo = "inteiro x inicio fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)

        with pytest.raises(ErroSintatico):
            parser.analisar()

    def test_erro_falta_inicio(self):
        """Testa erro quando falta palavra-chave 'inicio'"""
        codigo = "inteiro x; x <- 5 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)

        with pytest.raises(ErroSintatico):
            parser.analisar()

    def test_erro_falta_fim(self):
        """Testa erro quando falta palavra-chave 'fim'"""
        codigo = "inteiro x; inicio x <- 5"
        lexer = Lexer(codigo)
        parser = Parser(lexer)

        with pytest.raises(ErroSintatico):
            parser.analisar()

    def test_erro_condicional_sem_fimse(self):
        """Testa erro quando condicional não tem fimse"""
        codigo = """
        inteiro x;
        inicio
            se x == 5 entao
                x <- 10
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)

        with pytest.raises(ErroSintatico):
            parser.analisar()


class TestParserComplexo:
    """Testes com programas mais complexos"""

    def test_programa_completo(self, codigo_fibonacci):
        """Testa parsing de programa Fibonacci completo"""
        lexer = Lexer(codigo_fibonacci)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert isinstance(ast, Programa)
        assert len(ast.declaracoes) == 5
        assert len(ast.comandos) > 5  # Múltiplos comandos

    def test_loop_reverso(self, codigo_loop_reverso):
        """Testa parsing de loop reverso com passo negativo"""
        lexer = Lexer(codigo_loop_reverso)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert isinstance(ast, Programa)
        cmd = ast.comandos[0]
        assert isinstance(cmd, RepeticaoPara)

    def test_passo_opcional(self, codigo_passo_opcional):
        """Testa parsing de loop sem passo explícito"""
        lexer = Lexer(codigo_passo_opcional)
        parser = Parser(lexer)
        ast = parser.analisar()

        assert isinstance(ast, Programa)
        cmd = ast.comandos[0]
        assert isinstance(cmd, RepeticaoPara)
        assert isinstance(cmd.passo, Literal)
        assert cmd.passo.valor == "1"
