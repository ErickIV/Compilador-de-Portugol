"""
Analisador Léxico (Lexer) para a linguagem Portugol

Este módulo implementa a análise léxica, convertendo o código fonte
em uma sequência de tokens que serão processados pelo parser.

EXPRESSÕES REGULARES DOS TOKENS:
================================
Os tokens são reconhecidos seguindo os seguintes padrões (ERs):

1. IDENTIFICADORES:
   ER: [a-zA-Z_][a-zA-Z0-9_]*
   Descrição: Começa com letra ou underscore, seguido de letras, dígitos ou underscores
   Exemplos: variavel, soma_total, _valor, contador1

2. NÚMEROS INTEIROS:
   ER: [0-9]+
   Descrição: Um ou mais dígitos
   Exemplos: 0, 42, 1234

3. NÚMEROS REAIS:
   ER: [0-9]+\.[0-9]+
   Descrição: Um ou mais dígitos, ponto decimal, um ou mais dígitos
   Exemplos: 3.14, 0.5, 123.456

4. STRINGS (TEXTO):
   ER: "[^"]*"
   Descrição: Aspas duplas, zero ou mais caracteres não-aspas, aspas duplas
   Exemplos: "Hello", "Texto com espaços", ""

5. PALAVRAS-CHAVE:
   ER: (se|entao|senao|fimse|enquanto|faca|fimenquanto|leia|escreva|...)
   Descrição: Conjunto fixo de palavras reservadas da linguagem
   Exemplos: se, enquanto, leia, escreva

6. OPERADORES COMPOSTOS:
   ER: (<=|>=|==|!=|<-)
   Descrição: Operadores de dois caracteres
   Exemplos: <=, >=, ==, !=, <-

7. OPERADORES SIMPLES:
   ER: [+\-*/%^><]
   Descrição: Operadores aritméticos e relacionais de um caractere
   Exemplos: +, -, *, /, %, ^, <, >

8. DELIMITADORES:
   ER: [;,(){}]
   Descrição: Símbolos de pontuação e delimitação
   Exemplos: ;, ,, (, ), {, }

9. COMENTÁRIOS:
   - Linha: //[^\n]*
   - Bloco: /\*.*?\*/
   Descrição: Ignorados pelo analisador léxico
   Exemplos: // comentário, /* bloco */

NOTA: O lexer atual usa lógica imperativa direta (if/while) ao invés de
um AFD explícito, mas os padrões acima definem formalmente cada token.
"""

from typing import Dict, Optional
from .ast_nodes import TipoToken, Token
from .exceptions import ErroLexico


class Lexer:
    """
    Analisador léxico para a linguagem Portugol
    
    Responsável por:
    - Quebrar o código fonte em tokens
    - Identificar palavras-chave, operadores e literais
    - Ignorar espaços em branco e comentários
    - Rastrear posição (linha/coluna) para relatórios de erro
    """
    
    def __init__(self, codigo_fonte: str):
        self.codigo_fonte = codigo_fonte
        self.tamanho_codigo = len(codigo_fonte)
        self.posicao_atual = 0
        self.linha = 1
        self.coluna = 1
        
        # Mapeamento de palavras-chave para tipos de token
        self.palavras_chave: Dict[str, TipoToken] = {
            'se': TipoToken.SE,
            'entao': TipoToken.ENTAO,
            'senao': TipoToken.SENAO,
            'fimse': TipoToken.FIMSE,
            'enquanto': TipoToken.ENQUANTO,
            'fimenquanto': TipoToken.FIMENQUANTO,
            'para': TipoToken.PARA,
            'de': TipoToken.DE,
            'ate': TipoToken.ATE,
            'passo': TipoToken.PASSO,
            'fimpara': TipoToken.FIMPARA,
            'leia': TipoToken.LEIA,
            'escreva': TipoToken.ESCREVA,
            'inicio': TipoToken.INICIO,
            'fim': TipoToken.FIM,
            'inteiro': TipoToken.INTEIRO,
            'real': TipoToken.REAL,
            'caracter': TipoToken.CARACTER,
            'logico': TipoToken.LOGICO,
            'e': TipoToken.E,
            'ou': TipoToken.OU,
            'faca': TipoToken.FACA,
            'verdadeiro': TipoToken.VERDADEIRO,
            'falso': TipoToken.FALSO
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

    def _ignorar_espacos_e_comentarios(self) -> None:
        """Ignora espaços em branco e comentários"""
        while self.posicao_atual < self.tamanho_codigo:
            caractere = self._caractere_atual()
            
            # Espaços em branco
            if caractere.isspace():
                if caractere == '\n':
                    self.linha += 1
                    self.coluna = 1
                else:
                    self.coluna += 1
                self.posicao_atual += 1
                
            # Comentário de linha (//)
            elif caractere == '/' and self._proximo_caractere() == '/':
                while self.posicao_atual < self.tamanho_codigo and self._caractere_atual() != '\n':
                    self.posicao_atual += 1
                # Nova linha será processada na próxima iteração
                
            # Comentário de bloco (/* */)
            elif caractere == '/' and self._proximo_caractere() == '*':
                self.posicao_atual += 2
                while self.posicao_atual + 1 < self.tamanho_codigo:
                    if self._caractere_atual() == '*' and self._proximo_caractere() == '/':
                        self.posicao_atual += 2
                        break
                    if self._caractere_atual() == '\n':
                        self.linha += 1
                        self.coluna = 1
                    else:
                        self.coluna += 1
                    self.posicao_atual += 1
            else:
                break

    def _ler_identificador_ou_palavra_chave(self) -> Token:
        """Lê um identificador ou palavra-chave"""
        pos_inicial_coluna = self.coluna
        lexema = ''
        
        caractere = self._caractere_atual()
        while caractere is not None and (caractere.isalnum() or caractere == '_'):
            lexema += caractere
            self._avancar()
            caractere = self._caractere_atual()
            
        # Verifica se é palavra-chave ou identificador
        tipo = self.palavras_chave.get(lexema.lower(), TipoToken.IDENTIFICADOR)
        return Token(tipo, lexema, self.linha, pos_inicial_coluna)

    def _ler_numero(self) -> Token:
        """Lê um literal numérico (inteiro ou real)"""
        pos_inicial_coluna = self.coluna
        lexema = ''
        is_real = False
        
        caractere = self._caractere_atual()
        while caractere is not None and (caractere.isdigit() or caractere == '.'):
            if caractere == '.':
                if is_real:
                    raise ErroLexico("Número real inválido - múltiplos pontos decimais", 
                                   self.linha, self.coluna)
                is_real = True
            lexema += caractere
            self._avancar()
            caractere = self._caractere_atual()
            
        tipo = TipoToken.NUMERO_REAL if is_real else TipoToken.NUMERO_INTEIRO
        return Token(tipo, lexema, self.linha, pos_inicial_coluna)

    def _ler_string(self) -> Token:
        """Lê um literal de string"""
        pos_inicial_coluna = self.coluna
        self._avancar()  # Pula a primeira aspas
        lexema = ''
        
        while self._caractere_atual() is not None and self._caractere_atual() != '"':
            caractere = self._caractere_atual()
            if caractere == '\n':
                self.linha += 1
                self.coluna = 1
            lexema += caractere
            self._avancar()
            
        if self._caractere_atual() != '"':
            raise ErroLexico("String não fechada", self.linha, pos_inicial_coluna)
            
        self._avancar()  # Pula a aspas final
        return Token(TipoToken.TEXTO, lexema, self.linha, pos_inicial_coluna)

    def _ler_operador_composto(self) -> Optional[Token]:
        """Lê operadores compostos (<=, >=, ==, !=, <-)"""
        pos_inicial_coluna = self.coluna
        caractere = self._caractere_atual()
        proximo = self._proximo_caractere()
        
        if proximo == '=':
            self._avancar(2)
            if caractere == '<':
                return Token(TipoToken.MENOR_IGUAL, '<=', self.linha, pos_inicial_coluna)
            elif caractere == '>':
                return Token(TipoToken.MAIOR_IGUAL, '>=', self.linha, pos_inicial_coluna)
            elif caractere == '=':
                return Token(TipoToken.IGUAL, '==', self.linha, pos_inicial_coluna)
            elif caractere == '!':
                return Token(TipoToken.DIFERENTE, '!=', self.linha, pos_inicial_coluna)
                
        elif caractere == '<' and proximo == '-':
            self._avancar(2)
            return Token(TipoToken.ATRIBUICAO, '<-', self.linha, pos_inicial_coluna)
            
        return None

    def proximo_token(self) -> Token:
        """
        Retorna o próximo token do código fonte
        
        Returns:
            Token: O próximo token encontrado
            
        Raises:
            ErroLexico: Se encontrar um caractere inválido
        """
        self._ignorar_espacos_e_comentarios()
        
        if self.posicao_atual >= self.tamanho_codigo:
            return Token(TipoToken.EOF, 'EOF', self.linha, self.coluna)

        caractere = self._caractere_atual()
        pos_inicial_coluna = self.coluna

        # Identificadores e palavras-chave
        if caractere.isalpha() or caractere == '_':
            return self._ler_identificador_ou_palavra_chave()

        # Números
        if caractere.isdigit():
            return self._ler_numero()

        # Strings
        if caractere == '"':
            return self._ler_string()

        # Operadores compostos
        if caractere in ['<', '>', '=', '!']:
            operador_composto = self._ler_operador_composto()
            if operador_composto:
                return operador_composto
            
            # Operadores simples
            self._avancar()
            if caractere == '=':
                return Token(TipoToken.ATRIBUICAO, '=', self.linha, pos_inicial_coluna)
            elif caractere == '<':
                return Token(TipoToken.MENOR, '<', self.linha, pos_inicial_coluna)
            elif caractere == '>':
                return Token(TipoToken.MAIOR, '>', self.linha, pos_inicial_coluna)
            elif caractere == '!':
                raise ErroLexico("Operador '!' deve ser seguido de '='", 
                               self.linha, pos_inicial_coluna)

        # Símbolos simples
        simbolos_simples = {
            '(': TipoToken.ABRE_PARENTESES,
            ')': TipoToken.FECHA_PARENTESES,
            '{': TipoToken.ABRE_CHAVES,
            '}': TipoToken.FECHA_CHAVES,
            ';': TipoToken.PONTO_E_VIRGULA,
            ',': TipoToken.VIRGULA,
            '+': TipoToken.MAIS,
            '-': TipoToken.MENOS,
            '*': TipoToken.MULTIPLICACAO,
            '/': TipoToken.DIVISAO,
            '%': TipoToken.MODULO,
            '^': TipoToken.POTENCIA,
        }

        if caractere in simbolos_simples:
            self._avancar()
            return Token(simbolos_simples[caractere], caractere, self.linha, pos_inicial_coluna)

        # Caractere não reconhecido
        raise ErroLexico(f"Caractere inesperado '{caractere}'", self.linha, pos_inicial_coluna)