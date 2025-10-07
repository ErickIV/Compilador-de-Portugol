# =======================================================
# MÓDULO 1: ANÁLISE LÉXICA (LEXER)
# =======================================================

from enum import Enum
from typing import List, Optional, Union, Dict, Any
from dataclasses import dataclass
import re

# =======================================================
# EXCEÇÕES CUSTOMIZADAS
# =======================================================

class CompiladorError(Exception):
    """Classe base para erros do compilador"""
    def __init__(self, mensagem: str, linha: int = 0, coluna: int = 0):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(self._formatar_mensagem())
    
    def _formatar_mensagem(self) -> str:
        if self.linha > 0:
            return f"{self.mensagem} (linha {self.linha}, coluna {self.coluna})"
        return self.mensagem

class ErroLexico(CompiladorError):
    """Erro durante análise léxica"""
    pass

class ErroSintatico(CompiladorError):
    """Erro durante análise sintática"""
    pass

class ErroSemantico(CompiladorError):
    """Erro durante análise semântica"""
    pass

class TipoToken(Enum):
    SE = 1
    ENTAO = 2
    SENAO = 3
    FIMSE = 4
    ENQUANTO = 5
    FIMENQUANTO = 6
    PARA = 7
    FIMPARA = 8
    LEIA = 9
    ESCREVA = 10
    INICIO = 11
    FIM = 12
    INTEIRO = 13
    REAL = 14
    CARACTER = 15
    LOGICO = 16
    E = 17
    OU = 18
    ABRE_PARENTESES = 19
    FECHA_PARENTESES = 20
    ABRE_CHAVES = 21
    FECHA_CHAVES = 22
    VIRGULA = 23
    PONTO_E_VIRGULA = 24
    ATRIBUICAO = 25
    MAIOR = 26
    MENOR = 27
    MAIOR_IGUAL = 28
    MENOR_IGUAL = 29
    IGUAL = 30
    DIFERENTE = 31
    MAIS = 32
    MENOS = 33
    MULTIPLICACAO = 34
    DIVISAO = 35
    IDENTIFICADOR = 36
    NUMERO_INTEIRO = 37
    NUMERO_REAL = 38
    TEXTO = 39
    EOF = 40
    FACA = 41
    VERDADEIRO = 42
    FALSO = 43

@dataclass
class Token:
    """Representa um token léxico"""
    tipo: TipoToken
    valor: str
    linha: int
    coluna: int

    def __repr__(self) -> str:
        return f"Token(tipo={self.tipo.name}, valor='{self.valor}', linha={self.linha}, coluna={self.coluna})"

class Lexer:
    """Analisador léxico para a linguagem Portugol"""
    
    def __init__(self, codigo_fonte: str):
        self.codigo_fonte = codigo_fonte
        self.tamanho_codigo = len(codigo_fonte)
        self.posicao_atual = 0
        self.linha = 1
        self.coluna = 1
        self.palavras_chave: Dict[str, TipoToken] = {
            'se': TipoToken.SE, 'entao': TipoToken.ENTAO, 'senao': TipoToken.SENAO, 'fimse': TipoToken.FIMSE,
            'enquanto': TipoToken.ENQUANTO, 'fimenquanto': TipoToken.FIMENQUANTO, 'para': TipoToken.PARA,
            'fimpara': TipoToken.FIMPARA, 'leia': TipoToken.LEIA, 'escreva': TipoToken.ESCREVA,
            'inicio': TipoToken.INICIO, 'fim': TipoToken.FIM, 'inteiro': TipoToken.INTEIRO,
            'real': TipoToken.REAL, 'caracter': TipoToken.CARACTER, 'logico': TipoToken.LOGICO,
            'e': TipoToken.E, 'ou': TipoToken.OU, 'faca': TipoToken.FACA,
            'verdadeiro': TipoToken.VERDADEIRO, 'falso': TipoToken.FALSO
        }

    def _avancar(self, num_caracteres: int = 1) -> None:
        """Avança a posição atual no código fonte"""
        self.posicao_atual += num_caracteres
        self.coluna += num_caracteres

    def _caractere_atual(self) -> Optional[str]:
        """Retorna o caractere na posição atual ou None se fim do arquivo"""
        if self.posicao_atual < self.tamanho_codigo:
            return self.codigo_fonte[self.posicao_atual]
        return None

    def _proximo_caractere(self) -> Optional[str]:
        """Retorna o próximo caractere ou None se fim do arquivo"""
        if self.posicao_atual + 1 < self.tamanho_codigo:
            return self.codigo_fonte[self.posicao_atual + 1]
        return None

    def _ignorar_espacos_e_comentarios(self):
        while self.posicao_atual < self.tamanho_codigo:
            caractere = self._caractere_atual()
            if caractere.isspace():
                if caractere == '\n':
                    self.linha += 1
                    self.coluna = 1
                self.posicao_atual += 1
            elif caractere == '/' and self._proximo_caractere() == '/':
                while self.posicao_atual < self.tamanho_codigo and self._caractere_atual() != '\n':
                    self.posicao_atual += 1
                self.linha += 1
                self.coluna = 1
                self.posicao_atual += 1
            elif caractere == '/' and self._proximo_caractere() == '*':
                self.posicao_atual += 2
                while self.posicao_atual + 1 < self.tamanho_codigo and not (self._caractere_atual() == '*' and self._proximo_caractere() == '/'):
                    if self._caractere_atual() == '\n':
                        self.linha += 1
                        self.coluna = 1
                    self.posicao_atual += 1
                self.posicao_atual += 2
            else:
                break

    def proximo_token(self):
        self._ignorar_espacos_e_comentarios()
        if self.posicao_atual >= self.tamanho_codigo:
            return Token(TipoToken.EOF, 'EOF', self.linha, self.coluna)

        caractere = self._caractere_atual()
        pos_inicial_coluna = self.coluna

        if caractere.isalpha():
            lexema = ''
            while caractere is not None and (caractere.isalnum() or caractere == '_'):
                lexema += caractere
                self._avancar()
                caractere = self._caractere_atual()
            tipo = self.palavras_chave.get(lexema, TipoToken.IDENTIFICADOR)
            return Token(tipo, lexema, self.linha, pos_inicial_coluna)

        if caractere.isdigit():
            lexema = ''
            is_real = False
            while caractere is not None and (caractere.isdigit() or caractere == '.'):
                if caractere == '.':
                    if is_real:
                        raise ErroLexico("Número real inválido", self.linha, self.coluna)
                    is_real = True
                lexema += caractere
                self._avancar()
                caractere = self._caractere_atual()
            tipo = TipoToken.NUMERO_REAL if is_real else TipoToken.NUMERO_INTEIRO
            return Token(tipo, lexema, self.linha, pos_inicial_coluna)

        if caractere == '"':
            self._avancar()
            lexema = ''
            while self._caractere_atual() is not None and self._caractere_atual() != '"':
                lexema += self._caractere_atual()
                self._avancar()
            if self._caractere_atual() != '"':
                raise ErroLexico("String não fechada", self.linha, pos_inicial_coluna)
            self._avancar()
            return Token(TipoToken.TEXTO, lexema, self.linha, pos_inicial_coluna)

        if caractere in ['<', '>', '=', '!']:
            proximo = self._proximo_caractere()
            if proximo == '=':
                self._avancar(2)
                if caractere == '<': return Token(TipoToken.MENOR_IGUAL, '<=', self.linha, pos_inicial_coluna)
                if caractere == '>': return Token(TipoToken.MAIOR_IGUAL, '>=', self.linha, pos_inicial_coluna)
                if caractere == '=': return Token(TipoToken.IGUAL, '==', self.linha, pos_inicial_coluna)
                if caractere == '!': return Token(TipoToken.DIFERENTE, '!=', self.linha, pos_inicial_coluna)
            elif caractere == '<' and proximo == '-':
                self._avancar(2)
                return Token(TipoToken.ATRIBUICAO, '<-', self.linha, pos_inicial_coluna)
            else:
                # operadores simples
                if caractere == '=':
                    self._avancar()
                    return Token(TipoToken.ATRIBUICAO, '=', self.linha, pos_inicial_coluna)
                if caractere == '<':
                    self._avancar()
                    return Token(TipoToken.MENOR, '<', self.linha, pos_inicial_coluna)
                if caractere == '>':
                    self._avancar()
                    return Token(TipoToken.MAIOR, '>', self.linha, pos_inicial_coluna)
                if caractere == '!':
                    self._avancar()
                    raise ErroLexico("Operador '!' inválido", self.linha, pos_inicial_coluna)

        simbolos_simples = {
            '(': TipoToken.ABRE_PARENTESES, ')': TipoToken.FECHA_PARENTESES, '{': TipoToken.ABRE_CHAVES,
            '}': TipoToken.FECHA_CHAVES, ';': TipoToken.PONTO_E_VIRGULA, ',': TipoToken.VIRGULA,
            '+': TipoToken.MAIS, '-': TipoToken.MENOS, '*': TipoToken.MULTIPLICACAO, '/': TipoToken.DIVISAO,
            '=': TipoToken.ATRIBUICAO, '>': TipoToken.MAIOR, '<': TipoToken.MENOR
        }

        if caractere in simbolos_simples:
            self._avancar()
            return Token(simbolos_simples[caractere], caractere, self.linha, pos_inicial_coluna)

        raise ErroLexico(f"Caractere inesperado '{caractere}'", self.linha, pos_inicial_coluna)

# =======================================================
# MÓDULO 2: ANÁLISE SINTÁTICA (PARSER)
# =======================================================

class AST:
    """Classe base para nós da Árvore Sintática Abstrata"""
    pass

@dataclass
class Programa(AST):
    """Nó raiz do programa"""
    declaracoes: List[AST]

@dataclass
class DeclaracaoVariavel(AST):
    """Declaração de variáveis"""
    tipo: TipoToken
    nome_variaveis: List[str]

@dataclass
class Atribuicao(AST):
    """Atribuição de valor a variável"""
    nome: str
    valor: AST

@dataclass
class ChamadaFuncao(AST):
    """Chamada de função (leia/escreva)"""
    nome: str
    argumentos: List[AST]

@dataclass
class Se(AST):
    """Estrutura condicional se-então-senão"""
    condicao: AST
    bloco_se: AST
    bloco_senao: Optional[AST]

@dataclass
class Enquanto(AST):
    """Estrutura de repetição enquanto"""
    condicao: AST
    bloco: AST

@dataclass
class Identificador(AST):
    """Identificador de variável"""
    nome: str

@dataclass
class NumeroLiteral(AST):
    """Literal numérico"""
    valor: Union[int, float]

@dataclass
class StringLiteral(AST):
    """Literal de string"""
    valor: str

@dataclass
class Binario(AST):
    """Operação binária"""
    esquerda: AST
    operador: Token
    direita: AST

@dataclass
class Bloco(AST):
    """Bloco de declarações"""
    declaracoes: List[AST]

class Parser:
    """Parser para análise sintática da linguagem Portugol"""
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()
        self.bloco_atual = None

    def _consumir_token(self, tipo_esperado: TipoToken) -> None:
        """Consome um token do tipo esperado ou lança erro"""
        if self.token_atual.tipo == tipo_esperado:
            self.token_atual = self.lexer.proximo_token()
        else:
            raise ErroSintatico(
                f"Esperado {tipo_esperado.name}, mas encontrou {self.token_atual.tipo.name} em '{self.token_atual.valor}'",
                self.token_atual.linha, 
                self.token_atual.coluna
            )

    def parse_programa(self):
        declaracoes = []
        self._consumir_token(TipoToken.INICIO)
        while self.token_atual.tipo != TipoToken.FIM:
            declaracoes.append(self.parse_declaracao())
        self._consumir_token(TipoToken.FIM)
        self._consumir_token(TipoToken.EOF)
        return Programa(declaracoes)

    def parse_declaracao(self):
        token_tipo = self.token_atual.tipo
        if token_tipo in [TipoToken.INTEIRO, TipoToken.REAL, TipoToken.CARACTER, TipoToken.LOGICO]:
            self._consumir_token(token_tipo)
            nomes = []
            nomes.append(self.token_atual.valor)
            self._consumir_token(TipoToken.IDENTIFICADOR)
            while self.token_atual.tipo == TipoToken.VIRGULA:
                self._consumir_token(TipoToken.VIRGULA)
                nomes.append(self.token_atual.valor)
                self._consumir_token(TipoToken.IDENTIFICADOR)
            self._consumir_token(TipoToken.PONTO_E_VIRGULA)
            return DeclaracaoVariavel(token_tipo, nomes)

        elif token_tipo == TipoToken.SE:
            return self.parse_se()
        
        elif token_tipo == TipoToken.ENQUANTO:
            return self.parse_enquanto()
        
        elif token_tipo in [TipoToken.LEIA, TipoToken.ESCREVA]:
            return self.parse_comando()
        
        elif token_tipo == TipoToken.IDENTIFICADOR:
            # Só trata como atribuição se houver '=' ou '<-'
            nome_var = self.token_atual.valor
            self._consumir_token(TipoToken.IDENTIFICADOR)
            if self.token_atual.tipo in [TipoToken.ATRIBUICAO, TipoToken.IGUAL]:
                self._consumir_token(self.token_atual.tipo)
                valor = self.parse_expressao_ou_simples()
                self._consumir_token(TipoToken.PONTO_E_VIRGULA)
                return Atribuicao(nome_var, valor)
            self._consumir_token(TipoToken.PONTO_E_VIRGULA)
            return Identificador(nome_var)
        else:
            return self.parse_expressao_ou_simples()

    def parse_comando(self):
        """Comandos que terminam com ;"""
        if self.token_atual.tipo in [TipoToken.LEIA, TipoToken.ESCREVA]:
            nome_funcao = self.token_atual.valor
            self._consumir_token(self.token_atual.tipo)
            self._consumir_token(TipoToken.ABRE_PARENTESES)
            argumentos = self.parse_argumentos_funcao()
            self._consumir_token(TipoToken.FECHA_PARENTESES)
            self._consumir_token(TipoToken.PONTO_E_VIRGULA)
            return ChamadaFuncao(nome_funcao, argumentos)

        if self.token_atual.tipo == TipoToken.IDENTIFICADOR:
            nome_var = self.token_atual.valor
            self._consumir_token(TipoToken.IDENTIFICADOR)
            if self.token_atual.tipo in [TipoToken.ATRIBUICAO, TipoToken.IGUAL]:
                self._consumir_token(self.token_atual.tipo)
                valor = self.parse_expressao_ou_simples()
                self._consumir_token(TipoToken.PONTO_E_VIRGULA)
                return Atribuicao(nome_var, valor)
            self._consumir_token(TipoToken.PONTO_E_VIRGULA)
            return Identificador(nome_var)

        return self.parse_expressao_ou_simples()

    def parse_se(self):
        self._consumir_token(TipoToken.SE)
        self._consumir_token(TipoToken.ABRE_PARENTESES)
        condicao = self.parse_expressao_ou_simples()  # sem ponto e vírgula
        self._consumir_token(TipoToken.FECHA_PARENTESES)
        self._consumir_token(TipoToken.ENTAO)
        bloco_se = self.parse_bloco()
        bloco_senao = None
        if self.token_atual.tipo == TipoToken.SENAO:
            self._consumir_token(TipoToken.SENAO)
            if self.token_atual.tipo == TipoToken.SE:
                bloco_senao = self.parse_se()
            else:
                bloco_senao = self.parse_bloco()
        self._consumir_token(TipoToken.FIMSE)
        return Se(condicao, bloco_se, bloco_senao)

    def parse_enquanto(self):
        self._consumir_token(TipoToken.ENQUANTO)
        self._consumir_token(TipoToken.ABRE_PARENTESES)
        condicao = self.parse_expressao_ou_simples()  # sem ponto e vírgula
        self._consumir_token(TipoToken.FECHA_PARENTESES)
        self._consumir_token(TipoToken.FACA)
        bloco = self.parse_bloco()
        self._consumir_token(TipoToken.FIMENQUANTO)
        return Enquanto(condicao, bloco)

    def parse_bloco(self):
        delimitadores = {TipoToken.SENAO, TipoToken.FIMSE, TipoToken.FIM, TipoToken.FIMENQUANTO, TipoToken.FIMPARA}
        declaracoes = []
        while self.token_atual.tipo not in delimitadores:
            declaracoes.append(self.parse_declaracao())
        return Bloco(declaracoes)
        
    def parse_expressao(self):
        if self.token_atual.tipo in [TipoToken.LEIA, TipoToken.ESCREVA]:
            nome_funcao = self.token_atual.valor
            self._consumir_token(self.token_atual.tipo)
            self._consumir_token(TipoToken.ABRE_PARENTESES)
            argumentos = self.parse_argumentos_funcao()
            self._consumir_token(TipoToken.FECHA_PARENTESES)
            self._consumir_token(TipoToken.PONTO_E_VIRGULA)
            return ChamadaFuncao(nome_funcao, argumentos)

        if self.token_atual.tipo == TipoToken.IDENTIFICADOR:
            nome_var = self.token_atual.valor
            self._consumir_token(TipoToken.IDENTIFICADOR)
            if self.token_atual.tipo in [TipoToken.ATRIBUICAO, TipoToken.IGUAL]:
                self._consumir_token(self.token_atual.tipo)
                valor = self.parse_expressao_ou_simples()
                self._consumir_token(TipoToken.PONTO_E_VIRGULA)
                return Atribuicao(nome_var, valor)
            self._consumir_token(TipoToken.PONTO_E_VIRGULA)
            return Identificador(nome_var)

        return self.parse_expressao_ou_simples()

    def parse_expressao_ou_simples(self):
        return self.parse_expressao_logica()

    def parse_expressao_logica(self):
        """Analisa expressões lógicas (comparações e operadores lógicos)"""
        no = self.parse_expressao_comparativa()
        while self.token_atual.tipo in [TipoToken.E, TipoToken.OU]:
            operador = self.token_atual
            self._consumir_token(self.token_atual.tipo)
            no_direita = self.parse_expressao_comparativa()
            no = Binario(no, operador, no_direita)
        return no

    def parse_expressao_comparativa(self):
        """Analisa expressões de comparação (==, !=, <, >, <=, >=)"""
        no = self.parse_expressao_aditiva()
        while self.token_atual.tipo in [TipoToken.IGUAL, TipoToken.DIFERENTE, TipoToken.MAIOR, TipoToken.MENOR, TipoToken.MAIOR_IGUAL, TipoToken.MENOR_IGUAL]:
            operador = self.token_atual
            self._consumir_token(self.token_atual.tipo)
            no_direita = self.parse_expressao_aditiva()
            no = Binario(no, operador, no_direita)
        return no

    def parse_expressao_aditiva(self):
        no = self.parse_expressao_multiplicativa()
        while self.token_atual.tipo in [TipoToken.MAIS, TipoToken.MENOS]:
            operador = self.token_atual
            self._consumir_token(self.token_atual.tipo)
            no_direita = self.parse_expressao_multiplicativa()
            no = Binario(no, operador, no_direita)
        return no

    def parse_expressao_multiplicativa(self):
        no = self.parse_fator()
        while self.token_atual.tipo in [TipoToken.MULTIPLICACAO, TipoToken.DIVISAO]:
            operador = self.token_atual
            self._consumir_token(self.token_atual.tipo)
            no_direita = self.parse_fator()
            no = Binario(no, operador, no_direita)
        return no

    def parse_fator(self):
        """Analisa fatores: números, strings, identificadores, expressões entre parênteses"""
        token = self.token_atual
        
        # Suporte a números negativos
        if token.tipo == TipoToken.MENOS:
            self._consumir_token(TipoToken.MENOS)
            fator = self.parse_fator()  # recursivo para suportar --5, etc.
            if isinstance(fator, NumeroLiteral):
                return NumeroLiteral(-fator.valor)
            else:
                # Para expressões como -x, criar um nó binário (0 - x)
                return Binario(NumeroLiteral(0), Token(TipoToken.MENOS, '-', token.linha, token.coluna), fator)
        
        if token.tipo in [TipoToken.NUMERO_INTEIRO, TipoToken.NUMERO_REAL]:
            self._consumir_token(token.tipo)
            # Converter string para número apropriado
            valor = float(token.valor) if token.tipo == TipoToken.NUMERO_REAL else int(token.valor)
            return NumeroLiteral(valor)
        elif token.tipo == TipoToken.TEXTO:
            self._consumir_token(token.tipo)
            return StringLiteral(token.valor)
        elif token.tipo == TipoToken.IDENTIFICADOR:
            self._consumir_token(TipoToken.IDENTIFICADOR)
            return Identificador(token.valor)
        elif token.tipo == TipoToken.ABRE_PARENTESES:
            self._consumir_token(TipoToken.ABRE_PARENTESES)
            expressao = self.parse_expressao_ou_simples()
            self._consumir_token(TipoToken.FECHA_PARENTESES)
            return expressao
        elif token.tipo in [TipoToken.VERDADEIRO, TipoToken.FALSO]:
            self._consumir_token(token.tipo)
            valor = True if token.tipo == TipoToken.VERDADEIRO else False
            return NumeroLiteral(valor)  # Usando NumeroLiteral para boolean também
        
        raise ErroSintatico(f"Fator inesperado em '{token.valor}'", token.linha, token.coluna)

    def parse_argumentos_funcao(self):
        argumentos = []
        if self.token_atual.tipo != TipoToken.FECHA_PARENTESES:
            argumentos.append(self.parse_expressao_ou_simples())
            while self.token_atual.tipo == TipoToken.VIRGULA:
                self._consumir_token(TipoToken.VIRGULA)
                argumentos.append(self.parse_expressao_ou_simples())
        return argumentos

# =======================================================
# MÓDULO 3: ANÁLISE SEMÂNTICA
# =======================================================

class EntradaTabelaSimbolos:
    def __init__(self, nome, tipo):
        self.nome = nome
        self.tipo = tipo

class TabelaSimbolos:
    def __init__(self):
        self._escopo = [{}]

    def entrar_escopo(self):
        self._escopo.append({})

    def sair_escopo(self):
        if len(self._escopo) > 1:
            self._escopo.pop()

    def adicionar_simbolo(self, nome: str, tipo: TipoToken) -> None:
        """Adiciona um símbolo à tabela no escopo atual"""
        if nome in self._escopo[-1]:
            raise ErroSemantico(f"Variável '{nome}' já declarada neste escopo")
        self._escopo[-1][nome] = EntradaTabelaSimbolos(nome, tipo)

    def obter_simbolo(self, nome):
        for escopo in reversed(self._escopo):
            if nome in escopo:
                return escopo[nome]
        return None

class AnalisadorSemantico:
    def __init__(self, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos

    def visitar(self, no):
        nome_metodo = f"visitar_{type(no).__name__}"
        metodo = getattr(self, nome_metodo, self.visitar_padrao)
        resultado = metodo(no)
        return str(resultado) if resultado is not None else ""

    def visitar_padrao(self, no):
        for _, valor in no.__dict__.items():
            if isinstance(valor, list):
                for item in valor:
                    if isinstance(item, AST):
                        self.visitar(item)
            elif isinstance(valor, AST):
                self.visitar(valor)

    def visitar_Programa(self, no):
        self.visitar_padrao(no)

    def visitar_DeclaracaoVariavel(self, no):
        for nome in no.nome_variaveis:
            self.tabela_simbolos.adicionar_simbolo(nome, no.tipo)

    def visitar_Atribuicao(self, no: Atribuicao) -> None:
        """Valida atribuição de variável"""
        simbolo = self.tabela_simbolos.obter_simbolo(no.nome)
        if simbolo is None:
            raise ErroSemantico(f"Variável '{no.nome}' não declarada")
        
        valor_tipo = self.inferir_tipo(no.valor)
        if valor_tipo and simbolo.tipo != valor_tipo:
            # Permite conversão implícita entre tipos compatíveis
            conversoes_permitidas = [
                (TipoToken.INTEIRO, TipoToken.REAL),  # int -> real
                (TipoToken.REAL, TipoToken.INTEIRO),  # real -> int (com perda)
                (TipoToken.LOGICO, TipoToken.LOGICO)  # bool -> bool
            ]
            if (valor_tipo, simbolo.tipo) not in conversoes_permitidas:
                raise ErroSemantico(f"Tipo incompatível na atribuição de '{no.nome}'. Esperado {simbolo.tipo}, encontrado {valor_tipo}")
        
        self.visitar(no.valor)

    def inferir_tipo(self, no: AST) -> Optional[TipoToken]:
        """Infere o tipo de uma expressão"""
        if isinstance(no, NumeroLiteral):
            if isinstance(no.valor, bool):
                return TipoToken.LOGICO
            return TipoToken.REAL if '.' in str(no.valor) else TipoToken.INTEIRO
        if isinstance(no, StringLiteral):
            return TipoToken.CARACTER
        if isinstance(no, Identificador):
            simbolo = self.tabela_simbolos.obter_simbolo(no.nome)
            return simbolo.tipo if simbolo else None
        if isinstance(no, Binario):
            # Operadores de comparação retornam boolean
            if no.operador.tipo in [TipoToken.IGUAL, TipoToken.DIFERENTE, TipoToken.MAIOR, 
                                   TipoToken.MENOR, TipoToken.MAIOR_IGUAL, TipoToken.MENOR_IGUAL]:
                return TipoToken.LOGICO
            # Operadores lógicos retornam boolean
            if no.operador.tipo in [TipoToken.E, TipoToken.OU]:
                return TipoToken.LOGICO
        return None

    def visitar_ChamadaFuncao(self, no: ChamadaFuncao) -> None:
        """Valida chamadas de função"""
        if no.nome == "leia":
            for arg in no.argumentos:
                if not isinstance(arg, Identificador):
                    raise ErroSemantico("Argumento da função 'leia' deve ser uma variável")
                simbolo = self.tabela_simbolos.obter_simbolo(arg.nome)
                if simbolo is None:
                    raise ErroSemantico(f"Variável '{arg.nome}' não declarada")
        elif no.nome == "escreva":
            pass
        else:
            raise ErroSemantico(f"Função '{no.nome}' não reconhecida")

    def visitar_Se(self, no):
        self.tabela_simbolos.entrar_escopo()
        self.visitar(no.condicao)
        self.visitar(no.bloco_se)
        self.tabela_simbolos.sair_escopo()
        if no.bloco_senao:
            self.tabela_simbolos.entrar_escopo()
            self.visitar(no.bloco_senao)
            self.tabela_simbolos.sair_escopo()

    def visitar_Enquanto(self, no):
        self.tabela_simbolos.entrar_escopo()
        self.visitar(no.condicao)
        self.visitar(no.bloco)
        self.tabela_simbolos.sair_escopo()

    def visitar_Identificador(self, no: Identificador) -> None:
        """Valida se identificador foi declarado"""
        simbolo = self.tabela_simbolos.obter_simbolo(no.nome)
        if simbolo is None:
            raise ErroSemantico(f"Variável '{no.nome}' não declarada")

    def visitar_NumeroLiteral(self, no): 
        return str(no.valor)
    
    def visitar_StringLiteral(self, no): 
        return f"'{no.valor}'"
    
    def visitar_Binario(self, no): 
        self.visitar_padrao(no)
    
    def visitar_Bloco(self, no): 
        self.visitar_padrao(no)

# =======================================================
# MÓDULO 4: GERAÇÃO DE CÓDIGO
# =======================================================

class GeradorDeCodigo:
    def __init__(self, tabela_simbolos):
        self.tabela_simbolos = tabela_simbolos
        self.codigo_gerado = []
        self.indentacao = 0

    def _adicionar_linha(self, linha):
        indentacao = "    " * self.indentacao
        self.codigo_gerado.append(f"{indentacao}{linha}")

    def _entrar_escopo(self): self.indentacao += 1
    def _sair_escopo(self): self.indentacao -= 1

    def gerar(self, ast):
        self.visitar(ast)
        return "\n".join(self.codigo_gerado)
    
    def visitar(self, no):
        nome_metodo = f"visitar_{type(no).__name__}"
        metodo = getattr(self, nome_metodo, self.visitar_padrao)
        return metodo(no)

    def visitar_padrao(self, no):
        for _, valor in no.__dict__.items():
            if isinstance(valor, list):
                for item in valor:
                    if isinstance(item, AST):
                        self.visitar(item)
            elif isinstance(valor, AST):
                self.visitar(valor)

    def visitar_Programa(self, no): self.visitar_padrao(no)
    def visitar_Bloco(self, no): self.visitar_padrao(no)

    def visitar_DeclaracaoVariavel(self, no):
        tipo_py = '0'
        if no.tipo == TipoToken.REAL: tipo_py = '0.0'
        if no.tipo == TipoToken.CARACTER: tipo_py = "''"
        if no.tipo == TipoToken.LOGICO: tipo_py = "False"
        for nome in no.nome_variaveis:
            self._adicionar_linha(f"{nome} = {tipo_py}")
        
    def visitar_Atribuicao(self, no):
        valor = self.visitar(no.valor)
        self._adicionar_linha(f"{no.nome} = {valor}")

    def visitar_ChamadaFuncao(self, no):
        argumentos = []
        for arg in no.argumentos:
            argumentos.append(self.visitar(arg))
        
        if no.nome == "leia":
            var_node = no.argumentos[0]
            if isinstance(var_node, Identificador):
                simbolo = self.tabela_simbolos.obter_simbolo(var_node.nome)
                if simbolo is None:
                    raise Exception("Erro interno: Variável não encontrada na tabela de símbolos.")
                
                tipo_conversoes = {
                    TipoToken.INTEIRO: "int",
                    TipoToken.REAL: "float"
                }
                
                conversao = tipo_conversoes.get(simbolo.tipo, "")
                if conversao:
                    self._adicionar_linha(f"{var_node.nome} = {conversao}(input())")
                else:
                    self._adicionar_linha(f"{var_node.nome} = input()")
        elif no.nome == "escreva":
            args = [self.visitar(arg) for arg in no.argumentos]
            linha = "print(" + ", ".join(args) + ")"
            self._adicionar_linha(linha)

    def visitar_Se(self, no):
        condicao = self.visitar(no.condicao)
        self._adicionar_linha(f"if {condicao}:")
        self._entrar_escopo()
        self.visitar(no.bloco_se)
        self._sair_escopo()
        if no.bloco_senao:
            self._adicionar_linha("else:")
            self._entrar_escopo()
            self.visitar(no.bloco_senao)
            self._sair_escopo()

    def visitar_Enquanto(self, no):
        condicao = self.visitar(no.condicao)
        self._adicionar_linha(f"while {condicao}:")
        self._entrar_escopo()
        self.visitar(no.bloco)
        self._sair_escopo()

    def visitar_NumeroLiteral(self, no: NumeroLiteral) -> str:
        """Gera código para literais numéricos e booleanos"""
        if isinstance(no.valor, bool):
            return "True" if no.valor else "False"
        return str(no.valor)
    def visitar_StringLiteral(self, no): return f"'{no.valor}'"
    def visitar_Identificador(self, no): return no.nome
    def visitar_Binario(self, no: Binario) -> str:
        """Gera código para operações binárias"""
        esquerda = self.visitar(no.esquerda)
        direita = self.visitar(no.direita)
        
        operador_mapeamento = {
            '==': '==', '!=': '!=', '<': '<', '>': '>',
            '<=': '<=', '>=': '>=', '+': '+', '-': '-',
            '*': '*', '/': '/', 'e': 'and', 'ou': 'or'
        }
        operador = operador_mapeamento.get(no.operador.valor, no.operador.valor)
        
        return f"({esquerda} {operador} {direita})"

# =======================================================
# EXECUÇÃO DO COMPILADOR
# =======================================================

def compilar_e_executar():
    """Função principal que executa todas as fases do compilador"""
    try:
        with open('programa.por', 'r', encoding='utf-8') as arquivo:
            codigo_fonte = arquivo.read()

        print("--- Código Portugol ---")
        print(codigo_fonte)

        # 1. Análise Léxica
        lexer = Lexer(codigo_fonte)
        
        # 2. Análise Sintática
        parser = Parser(lexer)
        ast = parser.parse_programa()
        
        # 3. Análise Semântica
        tabela_simbolos = TabelaSimbolos()
        analisador_semantico = AnalisadorSemantico(tabela_simbolos)
        analisador_semantico.visitar(ast)
        
        # 4. Geração de Código
        gerador = GeradorDeCodigo(tabela_simbolos)
        codigo_python = gerador.gerar(ast)

        print("\n--- Código Python Gerado ---")
        print(codigo_python)

        print("\n--- Executando o Código Python ---")
        exec(codigo_python)

    except FileNotFoundError:
        print("Erro: O arquivo 'programa.por' não foi encontrado.")
        print("Crie um arquivo com esse nome e adicione o seu código Portugol.")
    except (ErroLexico, ErroSintatico, ErroSemantico) as e:
        print(f"Erro de compilação: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    compilar_e_executar()