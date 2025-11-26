"""
Testes de Integração End-to-End

Testa o pipeline completo de compilação desde o código Portugol
até a execução do código Python gerado.
"""

import pytest
import os
from src.main import CompiladorPortugol


class TestIntegracaoBasica:
    """Testes de integração básicos"""

    def test_compilacao_simples(self):
        """Testa compilação e execução de programa simples"""
        codigo = "inteiro x; inicio x <- 42 fim"
        compilador = CompiladorPortugol()

        # Deve compilar sem erros
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_compilacao_com_operacoes(self):
        """Testa compilação com operações aritméticas"""
        codigo = """
        inteiro a, b, c;
        inicio
            a <- 10
            b <- 20
            c <- a + b
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_compilacao_com_condicional(self):
        """Testa compilação com estrutura condicional"""
        codigo = """
        inteiro x;
        inicio
            x <- 5
            se x > 0 entao
                x <- x * 2
            fimse
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_compilacao_com_loop_enquanto(self):
        """Testa compilação com loop enquanto"""
        codigo = """
        inteiro x;
        inicio
            x <- 0
            enquanto x < 5 faca
                x <- x + 1
            fimenquanto
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True


class TestIntegracaoLoopPara:
    """Testes de integração para loop 'para'"""

    def test_loop_para_positivo(self):
        """Testa loop para com passo positivo"""
        codigo = """
        inteiro i, soma;
        inicio
            soma <- 0
            para i de 1 ate 10 passo 1 faca
                soma <- soma + i
            fimpara
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_loop_para_negativo(self):
        """Testa loop para com passo negativo"""
        codigo = """
        inteiro i, conta;
        inicio
            conta <- 0
            para i de 10 ate 1 passo -1 faca
                conta <- conta + 1
            fimpara
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_loop_para_sem_passo(self):
        """Testa loop para sem passo explícito (deve usar 1 como padrão)"""
        codigo = """
        inteiro i, soma;
        inicio
            soma <- 0
            para i de 1 ate 5 faca
                soma <- soma + i
            fimpara
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_loop_para_passo_2(self):
        """Testa loop para com passo 2"""
        codigo = """
        inteiro i;
        inicio
            para i de 0 ate 10 passo 2 faca
                escreva(i)
            fimpara
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True


class TestIntegracaoStringEscape:
    """Testes de strings com caracteres escapados"""

    def test_string_com_aspas_escapadas(self):
        """Testa string com aspas escapadas"""
        codigo = r'''
        caracter texto;
        inicio
            texto <- "Teste com \"aspas\" no meio"
            escreva(texto)
        fim
        '''
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_string_com_newline(self):
        """Testa string com newline escapado"""
        codigo = r'''
        caracter texto;
        inicio
            texto <- "Linha 1\nLinha 2"
            escreva(texto)
        fim
        '''
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True


class TestIntegracaoExemplos:
    """Testes com programas de exemplo"""

    def test_fibonacci(self, codigo_fibonacci):
        """Testa compilação do programa Fibonacci"""
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo_fibonacci)
        assert resultado is True

    def test_loop_reverso(self, codigo_loop_reverso):
        """Testa compilação de loop reverso"""
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo_loop_reverso)
        assert resultado is True

    def test_passo_opcional(self, codigo_passo_opcional):
        """Testa compilação com passo opcional"""
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo_passo_opcional)
        assert resultado is True


class TestIntegracaoExemplosArquivos:
    """Testes com arquivos de exemplo do repositório"""

    @pytest.mark.skipif(not os.path.exists("exemplos/fibonacci.por"),
                        reason="Arquivo de exemplo não encontrado")
    def test_exemplo_fibonacci(self):
        """Testa compilação do exemplo fibonacci.por"""
        compilador = CompiladorPortugol()
        sucesso = compilador.compilar_arquivo("exemplos/fibonacci.por")
        assert sucesso is True

    @pytest.mark.skipif(not os.path.exists("exemplos/fatorial.por"),
                        reason="Arquivo de exemplo não encontrado")
    def test_exemplo_fatorial(self):
        """Testa compilação do exemplo fatorial.por"""
        compilador = CompiladorPortugol()
        sucesso = compilador.compilar_arquivo("exemplos/fatorial.por")
        assert sucesso is True

    @pytest.mark.skipif(not os.path.exists("exemplos/teste_modulo.por"),
                        reason="Arquivo de exemplo não encontrado")
    def test_exemplo_modulo(self):
        """Testa compilação do exemplo teste_modulo.por"""
        compilador = CompiladorPortugol()
        sucesso = compilador.compilar_arquivo("exemplos/teste_modulo.por")
        assert sucesso is True

    @pytest.mark.skipif(not os.path.exists("exemplos/demo_completa.por"),
                        reason="Arquivo de exemplo não encontrado")
    def test_exemplo_demo_completa(self):
        """Testa compilação do exemplo demo_completa.por"""
        compilador = CompiladorPortugol()
        sucesso = compilador.compilar_arquivo("exemplos/demo_completa.por")
        assert sucesso is True


class TestIntegracaoOtimizacoes:
    """Testes com otimizações ativadas"""

    def test_compilacao_com_otimizacoes(self):
        """Testa compilação com otimizações ativadas"""
        codigo = """
        inteiro x, y, z;
        inicio
            x <- 5 + 3
            y <- x * 1
            z <- y + 0
        fim
        """
        compilador = CompiladorPortugol(otimizar=True, mostrar_intermediario=True)
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    @pytest.mark.skipif(not os.path.exists("exemplos/teste_otimizacoes.por"),
                        reason="Arquivo de exemplo não encontrado")
    def test_exemplo_otimizacoes(self):
        """Testa compilação do exemplo teste_otimizacoes.por com otimizações"""
        compilador = CompiladorPortugol(otimizar=True, mostrar_intermediario=True)
        sucesso = compilador.compilar_arquivo("exemplos/teste_otimizacoes.por")
        assert sucesso is True


class TestIntegracaoComplexo:
    """Testes com programas complexos"""

    def test_programa_aninhamento_profundo(self):
        """Testa programa com estruturas profundamente aninhadas"""
        codigo = """
        inteiro x, y, z;
        inicio
            x <- 1
            se x > 0 entao
                y <- 0
                enquanto y < 3 faca
                    para z de 1 ate 2 faca
                        x <- x + 1
                    fimpara
                    y <- y + 1
                fimenquanto
            fimse
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_programa_multiplas_variaveis(self):
        """Testa programa com muitas variáveis"""
        codigo = """
        inteiro a, b, c, d, e;
        real x, y, z;
        caracter nome, sobrenome;
        logico ativo, inativo;

        inicio
            a <- 1
            b <- 2
            c <- a + b
            x <- 3.14
            nome <- "Teste"
            ativo <- verdadeiro
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True

    def test_programa_todos_operadores(self):
        """Testa programa usando todos os tipos de operadores"""
        codigo = """
        inteiro a, b;
        real c;
        logico d, e, f;

        inicio
            a <- 10
            b <- 3

            c <- a + b
            c <- a - b
            c <- a * b
            c <- a / b
            c <- a % b
            c <- a ^ b

            d <- a == b
            d <- a != b
            d <- a < b
            d <- a <= b
            d <- a > b
            d <- a >= b

            e <- verdadeiro
            f <- falso
            d <- e e f
            d <- e ou f
        fim
        """
        compilador = CompiladorPortugol()
        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is True


class TestIntegracaoErros:
    """Testes de tratamento de erros"""

    def test_erro_variavel_nao_declarada(self):
        """Testa que erro de variável não declarada é capturado"""
        codigo = "inicio x <- 5 fim"
        compilador = CompiladorPortugol()

        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is False

    def test_erro_sintaxe(self):
        """Testa que erro de sintaxe é capturado"""
        codigo = "inteiro x inicio fim"  # Falta ponto-e-vírgula
        compilador = CompiladorPortugol()

        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is False

    def test_erro_lexico(self):
        """Testa que erro léxico é capturado"""
        codigo = "inteiro x; inicio x <- @ fim"  # @ é inválido
        compilador = CompiladorPortugol()

        resultado = compilador.executar_compilacao_e_teste(codigo)
        assert resultado is False
