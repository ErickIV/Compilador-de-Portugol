import pytest
from src.lexer import Lexer
from src.ast_nodes import TipoToken
from src.exceptions import ErroLexico

def test_lexer_basico():
    codigo = "inteiro x = 10"
    lexer = Lexer(codigo)
    
    t1 = lexer.proximo_token()
    assert t1.tipo == TipoToken.INTEIRO
    
    t2 = lexer.proximo_token()
    assert t2.tipo == TipoToken.IDENTIFICADOR
    assert t2.lexema == "x"
    
    t3 = lexer.proximo_token()
    assert t3.tipo == TipoToken.ATRIBUICAO
    
    t4 = lexer.proximo_token()
    assert t4.tipo == TipoToken.NUMERO_INTEIRO
    assert t4.lexema == "10"

def test_string_simples():
    codigo = 'escreva("Ola Mundo")'
    lexer = Lexer(codigo)
    lexer.proximo_token() # escreva
    lexer.proximo_token() # (
    
    t_str = lexer.proximo_token()
    assert t_str.tipo == TipoToken.TEXTO
    assert t_str.lexema == "Ola Mundo"

def test_string_com_aspas_escapadas():
    # Testa que o lexer processa corretamente aspas escapadas
    codigo = 'escreva("Ola \\"Mundo\\"")'
    lexer = Lexer(codigo)
    lexer.proximo_token() # escreva
    lexer.proximo_token() # (
    
    t_str = lexer.proximo_token()
    assert t_str.tipo == TipoToken.TEXTO
    # Aspas escapadas devem resultar em aspas normais no lexema
    assert t_str.lexema == 'Ola "Mundo"'
