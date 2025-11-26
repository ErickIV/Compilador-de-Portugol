import sys
import os
import pytest

# Adiciona o diretório raiz ao PYTHONPATH para importar os módulos src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lexer import Lexer
from src.parser import Parser
from src.semantic import AnalisadorSemantico
from src.codegen import GeradorDeCodigo


@pytest.fixture
def lexer_simples():
    """Fixture que retorna um lexer com código simples"""
    codigo = "inteiro x; inicio x <- 5 fim"
    return Lexer(codigo)


@pytest.fixture
def parser_simples():
    """Fixture que retorna um parser com código simples"""
    codigo = "inteiro x; inicio x <- 5 fim"
    lexer = Lexer(codigo)
    return Parser(lexer)


@pytest.fixture
def codigo_fibonacci():
    """Fixture com código Fibonacci para testes"""
    return """
inteiro n, fib_anterior, fib_atual, fib_proximo, i;

inicio
    n <- 10
    fib_anterior <- 0
    fib_atual <- 1

    escreva("Fibonacci:", fib_anterior, fib_atual)

    para i de 2 ate n passo 1 faca
        fib_proximo <- fib_anterior + fib_atual
        escreva(fib_proximo)
        fib_anterior <- fib_atual
        fib_atual <- fib_proximo
    fimpara
fim
"""


@pytest.fixture
def codigo_loop_reverso():
    """Fixture com loop reverso para testar passo negativo"""
    return """
inteiro i;

inicio
    para i de 10 ate 1 passo -1 faca
        escreva(i)
    fimpara
fim
"""


@pytest.fixture
def codigo_passo_opcional():
    """Fixture com loop sem passo explícito"""
    return """
inteiro i;

inicio
    para i de 1 ate 5 faca
        escreva(i)
    fimpara
fim
"""
