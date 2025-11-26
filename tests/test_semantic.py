"""
Testes para o Analisador Semântico

Valida regras semânticas como declaração de variáveis,
verificação de tipos e inicialização.
"""

import pytest
import warnings
from src.lexer import Lexer
from src.parser import Parser
from src.semantic import AnalisadorSemantico, TabelaSimbolos
from src.exceptions import ErroSemantico


class TestTabelaSimbolos:
    """Testes para a Tabela de Símbolos"""

    def test_declarar_variavel(self):
        """Testa declaração de variável na tabela"""
        tabela = TabelaSimbolos()
        tabela.declarar_variavel("x", "inteiro", 1, 1)

        assert "x" in tabela.simbolos
        assert tabela.simbolos["x"]["tipo"] == "inteiro"
        assert tabela.simbolos["x"]["inicializada"] == False

    def test_declarar_variavel_duplicada(self):
        """Testa erro ao declarar variável duplicada"""
        tabela = TabelaSimbolos()
        tabela.declarar_variavel("x", "inteiro", 1, 1)

        with pytest.raises(ErroSemantico) as exc_info:
            tabela.declarar_variavel("x", "real", 2, 1)

        assert "já foi declarada" in str(exc_info.value)

    def test_verificar_variavel_declarada(self):
        """Testa verificação de variável declarada"""
        tabela = TabelaSimbolos()
        tabela.declarar_variavel("x", "inteiro", 1, 1)

        tipo = tabela.verificar_variavel_declarada("x", 2, 1)
        assert tipo == "inteiro"

    def test_verificar_variavel_nao_declarada(self):
        """Testa erro ao usar variável não declarada"""
        tabela = TabelaSimbolos()

        with pytest.raises(ErroSemantico) as exc_info:
            tabela.verificar_variavel_declarada("x", 1, 1)

        assert "não foi declarada" in str(exc_info.value)

    def test_marcar_como_inicializada(self):
        """Testa marcação de variável como inicializada"""
        tabela = TabelaSimbolos()
        tabela.declarar_variavel("x", "inteiro", 1, 1)

        assert tabela.simbolos["x"]["inicializada"] == False

        tabela.marcar_como_inicializada("x")
        assert tabela.simbolos["x"]["inicializada"] == True

    def test_verificar_inicializada_warning(self):
        """Testa warning para variável não inicializada"""
        tabela = TabelaSimbolos()
        tabela.declarar_variavel("x", "inteiro", 1, 1)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            tabela.verificar_inicializada("x", 2, 1)

            assert len(w) == 1
            assert "não foi inicializada" in str(w[0].message) or "antes de ser inicializada" in str(w[0].message)


class TestAnalisadorSemantico:
    """Testes para o Analisador Semântico"""

    def test_analise_programa_simples(self):
        """Testa análise semântica de programa simples"""
        codigo = "inteiro x; inicio x <- 5 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        # Não deve lançar exceção
        analisador.analisar(ast)

    def test_variavel_nao_declarada(self):
        """Testa erro quando variável não está declarada"""
        codigo = "inteiro x; inicio y <- 5 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        with pytest.raises(ErroSemantico) as exc_info:
            analisador.analisar(ast)

        assert "não foi declarada" in str(exc_info.value)

    def test_uso_antes_atribuicao_warning(self):
        """Testa warning quando variável é usada antes de ser inicializada"""
        codigo = "inteiro x, y; inicio y <- x fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            analisador.analisar(ast)

            # Deve emitir warning sobre 'x' não inicializado
            assert len(w) >= 1

    def test_atribuicao_inicializa_variavel(self):
        """Testa que atribuição marca variável como inicializada"""
        codigo = "inteiro x, y; inicio x <- 5 y <- x fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        # x foi inicializado antes de ser usado em y <- x
        assert analisador.tabela_simbolos.simbolos["x"]["inicializada"]
        assert analisador.tabela_simbolos.simbolos["y"]["inicializada"]

    def test_entrada_inicializa_variavel(self):
        """Testa que comando leia() marca variável como inicializada"""
        codigo = "inteiro x; inicio leia(x) fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        assert analisador.tabela_simbolos.simbolos["x"]["inicializada"]

    def test_variavel_em_expressao(self):
        """Testa uso de variável em expressão"""
        codigo = "inteiro x, y, z; inicio x <- 5 y <- 10 z <- x + y fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        # Todas as variáveis devem estar inicializadas
        assert all(
            analisador.tabela_simbolos.simbolos[v]["inicializada"]
            for v in ["x", "y", "z"]
        )

    def test_condicional_variavel_condicao(self):
        """Testa uso de variável em condição"""
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

    def test_repeticao_enquanto(self):
        """Testa análise de loop enquanto"""
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

    def test_repeticao_para(self):
        """Testa análise de loop para"""
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

        # Variável de loop é inicializada pelo próprio loop
        assert analisador.tabela_simbolos.simbolos["i"]["inicializada"]

    def test_repeticao_para_variavel_nao_declarada(self):
        """Testa erro quando variável de loop não está declarada"""
        codigo = """
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
        with pytest.raises(ErroSemantico):
            analisador.analisar(ast)

    def test_saida_multiplas_expressoes(self):
        """Testa comando escreva com múltiplas expressões"""
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

    def test_programa_completo(self, codigo_fibonacci):
        """Testa análise semântica de programa completo"""
        lexer = Lexer(codigo_fibonacci)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        # Todas as variáveis devem estar declaradas
        assert all(
            v in analisador.tabela_simbolos.simbolos
            for v in ["n", "fib_anterior", "fib_atual", "fib_proximo", "i"]
        )


class TestAnalisadorSemanticoTipos:
    """Testes para verificação de tipos"""

    def test_tipos_diferentes(self):
        """Testa que diferentes tipos podem ser declarados"""
        codigo = """
        inteiro i;
        real x;
        caracter nome;
        logico ativo;
        inicio
            i <- 42
            x <- 3.14
            nome <- "teste"
            ativo <- verdadeiro
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        assert analisador.tabela_simbolos.simbolos["i"]["tipo"] == "inteiro"
        assert analisador.tabela_simbolos.simbolos["x"]["tipo"] == "real"
        assert analisador.tabela_simbolos.simbolos["nome"]["tipo"] == "caracter"
        assert analisador.tabela_simbolos.simbolos["ativo"]["tipo"] == "logico"

    def test_obter_tipo_variavel(self):
        """Testa obtenção do tipo de uma variável"""
        codigo = "inteiro x; inicio x <- 5 fim"
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

        tipo = analisador.tabela_simbolos.obter_tipo("x")
        assert tipo == "inteiro"


class TestAnalisadorSemanticoComplexo:
    """Testes com programas mais complexos"""

    def test_loop_reverso(self, codigo_loop_reverso):
        """Testa análise semântica de loop reverso"""
        lexer = Lexer(codigo_loop_reverso)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

    def test_passo_opcional(self, codigo_passo_opcional):
        """Testa análise semântica com passo opcional"""
        lexer = Lexer(codigo_passo_opcional)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)

    def test_aninhamento_profundo(self):
        """Testa estruturas aninhadas profundamente"""
        codigo = """
        inteiro x, y;
        inicio
            x <- 1
            se x > 0 entao
                enquanto x < 5 faca
                    para y de 1 ate 3 passo 1 faca
                        escreva(x, y)
                    fimpara
                    x <- x + 1
                fimenquanto
            fimse
        fim
        """
        lexer = Lexer(codigo)
        parser = Parser(lexer)
        ast = parser.analisar()

        analisador = AnalisadorSemantico()
        analisador.analisar(ast)
