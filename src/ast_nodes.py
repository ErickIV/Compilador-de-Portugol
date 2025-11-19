"""
Definições dos nós da Árvore Sintática Abstrata (AST)

Este módulo contém todas as classes que representam os diferentes
tipos de nós na AST gerada pelo parser.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union
from enum import Enum


class TipoToken(Enum):
    """Enumeração dos tipos de tokens da linguagem Portugol"""
    # Palavras-chave
    SE = "se"
    ENTAO = "entao"
    SENAO = "senao"
    FIMSE = "fimse"
    ENQUANTO = "enquanto"
    FACA = "faca"
    FIMENQUANTO = "fimenquanto"
    PARA = "para"
    DE = "de"
    ATE = "ate"
    PASSO = "passo"
    FIMPARA = "fimpara"
    LEIA = "leia"
    ESCREVA = "escreva"
    INICIO = "inicio"
    FIM = "fim"
    
    # Tipos de dados
    INTEIRO = "inteiro"
    REAL = "real"
    CARACTER = "caracter"
    LOGICO = "logico"
    
    # Valores booleanos
    VERDADEIRO = "verdadeiro"
    FALSO = "falso"
    
    # Operadores lógicos
    E = "e"
    OU = "ou"
    
    # Símbolos
    MAIS = "+"
    MENOS = "-"
    MULTIPLICACAO = "*"
    DIVISAO = "/"
    MODULO = "%"
    POTENCIA = "^"
    ATRIBUICAO = "<-"
    IGUAL = "=="
    DIFERENTE = "!="
    MENOR = "<"
    MENOR_IGUAL = "<="
    MAIOR = ">"
    MAIOR_IGUAL = ">="
    ABRE_PARENTESES = "("
    FECHA_PARENTESES = ")"
    ABRE_CHAVES = "{"
    FECHA_CHAVES = "}"
    PONTO_E_VIRGULA = ";"
    VIRGULA = ","
    
    # Literais
    NUMERO_INTEIRO = "numero_inteiro"
    NUMERO_REAL = "numero_real"
    TEXTO = "texto"
    
    # Identificadores
    IDENTIFICADOR = "identificador"
    
    # Fim do arquivo
    EOF = "eof"


@dataclass
class Token:
    """Representa um token encontrado durante a análise léxica"""
    tipo: TipoToken
    lexema: str
    linha: int
    coluna: int


@dataclass
class AST:
    """Classe base para todos os nós da Árvore Sintática Abstrata"""
    pass


@dataclass
class Comando(AST):
    """Classe base para todos os comandos"""
    pass


@dataclass
class Expressao(AST):
    """Classe base para todas as expressões"""
    pass


@dataclass
class Programa(AST):
    """Nó raiz da AST representando o programa completo"""
    declaracoes: List['DeclaracaoVariavel']
    comandos: List[Comando]


@dataclass
class DeclaracaoVariavel(AST):
    """Declaração de uma variável com seu tipo"""
    tipo: str
    nome: str


@dataclass
class Atribuicao(Comando):
    """Comando de atribuição: variavel <- expressao"""
    variavel: str
    expressao: Expressao


@dataclass
class Condicional(Comando):
    """Comando condicional: se-entao-senao-fimse"""
    condicao: Expressao
    comandos_entao: List[Comando]
    comandos_senao: List[Comando] = field(default_factory=list)


@dataclass
class Repeticao(Comando):
    """Comando de repetição: enquanto-faca-fimenquanto"""
    condicao: Expressao
    comandos: List[Comando]


@dataclass
class RepeticaoPara(Comando):
    """Comando de repetição: para-de-ate-passo-faca-fimpara"""
    variavel: str
    inicio: Expressao
    fim: Expressao
    passo: Expressao
    comandos: List[Comando]


@dataclass
class Entrada(Comando):
    """Comando de entrada: leia(variavel)"""
    variavel: str


@dataclass
class Saida(Comando):
    """Comando de saída: escreva(expressao, ...)"""
    expressoes: List[Expressao]


@dataclass
class ExpressaoBinaria(Expressao):
    """Expressão binária: esquerda operador direita"""
    esquerda: Expressao
    operador: str
    direita: Expressao


@dataclass
class ExpressaoUnaria(Expressao):
    """Expressão unária: operador operando"""
    operador: str
    operando: Expressao


@dataclass
class Literal(Expressao):
    """Literal (número, string, booleano)"""
    valor: str


@dataclass
class Variavel(Expressao):
    """Referência a uma variável"""
    nome: str