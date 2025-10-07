# Pacote do compilador Portugol
"""
Compilador para linguagem Portugol
Desenvolvido como projeto acadêmico

Módulos:
- lexer: Análise léxica (tokenização)
- parser: Análise sintática (geração de AST)
- semantic: Análise semântica (validação de tipos)
- codegen: Geração de código Python
- ast_nodes: Definições dos nós da AST
- exceptions: Exceções customizadas do compilador
"""

__version__ = "1.0.0"
__author__ = "Estudante de Compiladores"

# Exportar classes principais para facilitar importação
from .main import CompiladorPortugol
from .exceptions import CompiladorError, ErroLexico, ErroSintatico, ErroSemantico
from .lexer import Lexer
from .parser import Parser
from .semantic import AnalisadorSemantico
from .codegen import GeradorDeCodigo

__all__ = [
    'CompiladorPortugol',
    'CompiladorError', 'ErroLexico', 'ErroSintatico', 'ErroSemantico',
    'Lexer', 'Parser', 'AnalisadorSemantico', 'GeradorDeCodigo'
]