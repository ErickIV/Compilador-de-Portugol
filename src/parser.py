"""
Analisador Sintático (Parser) para a linguagem Portugol

Este módulo implementa a análise sintática usando descida recursiva,
convertendo a sequência de tokens em uma Árvore Sintática Abstrata (AST).
"""

from typing import List, Optional
from .ast_nodes import (
    TipoToken, Token, Programa, DeclaracaoVariavel,
    Comando, Atribuicao, Condicional, Repeticao, RepeticaoPara, Entrada, Saida,
    Expressao, ExpressaoBinaria, ExpressaoUnaria, Literal, Variavel
)
from .lexer import Lexer
from .exceptions import ErroSintatico


class Parser:
    """
    Analisador sintático para a linguagem Portugol
    
    Implementa análise sintática descendente recursiva baseada na gramática:
    - programa -> declaracoes inicio comandos fim
    - declaracoes -> (tipo lista_vars ";")*
    - comando -> atribuicao | estrutura_controle | entrada_saida
    """
    
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.token_atual = self.lexer.proximo_token()

    def _avancar(self) -> None:
        """Avança para o próximo token"""
        self.token_atual = self.lexer.proximo_token()

    def _esperar_token(self, tipo_esperado: TipoToken) -> Token:
        """
        Verifica se o token atual é do tipo esperado
        
        Args:
            tipo_esperado: Tipo de token esperado
            
        Returns:
            Token: O token atual
            
        Raises:
            ErroSintatico: Se o token não for do tipo esperado
        """
        if self.token_atual.tipo != tipo_esperado:
            raise ErroSintatico(
                f"Esperado '{tipo_esperado.value}', encontrado '{self.token_atual.lexema}'",
                self.token_atual.linha,
                self.token_atual.coluna
            )
        token = self.token_atual
        self._avancar()
        return token

    def analisar(self) -> Programa:
        """
        Analisa o programa completo e retorna a AST
        
        Returns:
            Programa: Nó raiz da AST
        """
        declaracoes = self._analisar_declaracoes()
        self._esperar_token(TipoToken.INICIO)
        comandos = self._analisar_comandos()
        self._esperar_token(TipoToken.FIM)
        self._esperar_token(TipoToken.EOF)
        
        return Programa(declaracoes, comandos)

    def _analisar_declaracoes(self) -> List[DeclaracaoVariavel]:
        """Analisa declarações de variáveis"""
        declaracoes = []
        
        # Tipos válidos para declaração
        tipos_validos = {TipoToken.INTEIRO, TipoToken.REAL, TipoToken.CARACTER, TipoToken.LOGICO}
        
        while self.token_atual.tipo in tipos_validos:
            tipo = self.token_atual.lexema
            self._avancar()
            
            # Lista de variáveis separadas por vírgula
            nomes = []
            nomes.append(self._esperar_token(TipoToken.IDENTIFICADOR).lexema)
            
            while self.token_atual.tipo == TipoToken.VIRGULA:
                self._avancar()
                nomes.append(self._esperar_token(TipoToken.IDENTIFICADOR).lexema)
            
            self._esperar_token(TipoToken.PONTO_E_VIRGULA)
            
            # Cria uma declaração para cada variável
            for nome in nomes:
                declaracoes.append(DeclaracaoVariavel(tipo, nome))
        
        return declaracoes

    def _analisar_comandos(self) -> List[Comando]:
        """Analisa uma sequência de comandos"""
        comandos = []
        
        while self.token_atual.tipo != TipoToken.FIM:
            comando = self._analisar_comando()
            if comando:
                comandos.append(comando)
        
        return comandos

    def _analisar_comando(self) -> Optional[Comando]:
        """Analisa um comando individual"""
        if self.token_atual.tipo == TipoToken.IDENTIFICADOR:
            return self._analisar_atribuicao()
        elif self.token_atual.tipo == TipoToken.SE:
            return self._analisar_condicional()
        elif self.token_atual.tipo == TipoToken.ENQUANTO:
            return self._analisar_repeticao()
        elif self.token_atual.tipo == TipoToken.PARA:
            return self._analisar_repeticao_para()
        elif self.token_atual.tipo == TipoToken.LEIA:
            return self._analisar_entrada()
        elif self.token_atual.tipo == TipoToken.ESCREVA:
            return self._analisar_saida()
        else:
            # Token não reconhecido como início de comando
            if self.token_atual.tipo != TipoToken.FIM:
                raise ErroSintatico(
                    f"Comando inesperado '{self.token_atual.lexema}'",
                    self.token_atual.linha,
                    self.token_atual.coluna
                )
            return None

    def _analisar_atribuicao(self) -> Atribuicao:
        """Analisa comando de atribuição: variavel <- expressao"""
        token_var = self._esperar_token(TipoToken.IDENTIFICADOR)
        nome_variavel = token_var.lexema
        self._esperar_token(TipoToken.ATRIBUICAO)
        expressao = self._analisar_expressao()
        atrib = Atribuicao(nome_variavel, expressao)
        # Adicionar informações de localização dinamicamente
        atrib.linha = token_var.linha
        atrib.coluna = token_var.coluna
        return atrib

    def _analisar_condicional(self) -> Condicional:
        """Analisa comando condicional: se condicao entao comandos [senao comandos] fimse"""
        self._esperar_token(TipoToken.SE)
        condicao = self._analisar_expressao()
        self._esperar_token(TipoToken.ENTAO)
        
        comandos_entao = []
        while self.token_atual.tipo not in {TipoToken.SENAO, TipoToken.FIMSE}:
            comando = self._analisar_comando()
            if comando:
                comandos_entao.append(comando)
        
        comandos_senao = []
        if self.token_atual.tipo == TipoToken.SENAO:
            self._avancar()
            while self.token_atual.tipo != TipoToken.FIMSE:
                comando = self._analisar_comando()
                if comando:
                    comandos_senao.append(comando)
        
        self._esperar_token(TipoToken.FIMSE)
        return Condicional(condicao, comandos_entao, comandos_senao)

    def _analisar_repeticao(self) -> Repeticao:
        """Analisa comando de repetição: enquanto condicao faca comandos fimenquanto"""
        self._esperar_token(TipoToken.ENQUANTO)
        condicao = self._analisar_expressao()
        self._esperar_token(TipoToken.FACA)

        comandos = []
        while self.token_atual.tipo != TipoToken.FIMENQUANTO:
            comando = self._analisar_comando()
            if comando:
                comandos.append(comando)

        self._esperar_token(TipoToken.FIMENQUANTO)
        return Repeticao(condicao, comandos)

    def _analisar_repeticao_para(self) -> RepeticaoPara:
        """Analisa comando de repetição: para variavel de inicio ate fim [passo incremento] faca comandos fimpara

        Nota: A cláusula 'passo' é opcional. Se omitida, o passo padrão é 1.
        """
        self._esperar_token(TipoToken.PARA)
        variavel = self._esperar_token(TipoToken.IDENTIFICADOR).lexema
        self._esperar_token(TipoToken.DE)
        inicio = self._analisar_expressao()
        self._esperar_token(TipoToken.ATE)
        fim = self._analisar_expressao()

        # Passo é opcional - padrão é 1
        if self.token_atual.tipo == TipoToken.PASSO:
            self._avancar()
            passo = self._analisar_expressao()
        else:
            passo = Literal("1")

        self._esperar_token(TipoToken.FACA)

        comandos = []
        while self.token_atual.tipo != TipoToken.FIMPARA:
            comando = self._analisar_comando()
            if comando:
                comandos.append(comando)

        self._esperar_token(TipoToken.FIMPARA)
        return RepeticaoPara(variavel, inicio, fim, passo, comandos)

    def _analisar_entrada(self) -> Entrada:
        """Analisa comando de entrada: leia(variavel)"""
        token_leia = self._esperar_token(TipoToken.LEIA)
        self._esperar_token(TipoToken.ABRE_PARENTESES)
        nome_variavel = self._esperar_token(TipoToken.IDENTIFICADOR).lexema
        self._esperar_token(TipoToken.FECHA_PARENTESES)
        entrada = Entrada(nome_variavel)
        # Adicionar informações de localização dinamicamente
        entrada.linha = token_leia.linha
        entrada.coluna = token_leia.coluna
        return entrada

    def _analisar_saida(self) -> Saida:
        """Analisa comando de saída: escreva(expressao1, expressao2, ...)"""
        self._esperar_token(TipoToken.ESCREVA)
        self._esperar_token(TipoToken.ABRE_PARENTESES)
        
        expressoes = []
        expressoes.append(self._analisar_expressao())
        
        while self.token_atual.tipo == TipoToken.VIRGULA:
            self._avancar()
            expressoes.append(self._analisar_expressao())
        
        self._esperar_token(TipoToken.FECHA_PARENTESES)
        return Saida(expressoes)

    def _analisar_expressao(self) -> Expressao:
        """
        Analisa expressão lógica (precedência mais baixa)
        expressao -> expr_e (ou expr_e)*
        """
        esquerda = self._analisar_expressao_e()
        
        while self.token_atual.tipo == TipoToken.OU:
            operador = self.token_atual.lexema
            self._avancar()
            direita = self._analisar_expressao_e()
            esquerda = ExpressaoBinaria(esquerda, operador, direita)
        
        return esquerda

    def _analisar_expressao_e(self) -> Expressao:
        """
        Analisa expressão com operador 'e'
        expr_e -> expr_relacional (e expr_relacional)*
        """
        esquerda = self._analisar_expressao_relacional()
        
        while self.token_atual.tipo == TipoToken.E:
            operador = self.token_atual.lexema
            self._avancar()
            direita = self._analisar_expressao_relacional()
            esquerda = ExpressaoBinaria(esquerda, operador, direita)
        
        return esquerda

    def _analisar_expressao_relacional(self) -> Expressao:
        """
        Analisa expressão relacional
        expr_relacional -> expr_aritmetica (op_relacional expr_aritmetica)?
        """
        esquerda = self._analisar_expressao_aritmetica()
        
        ops_relacionais = {
            TipoToken.IGUAL, TipoToken.DIFERENTE,
            TipoToken.MENOR, TipoToken.MENOR_IGUAL,
            TipoToken.MAIOR, TipoToken.MAIOR_IGUAL
        }
        
        if self.token_atual.tipo in ops_relacionais:
            operador = self.token_atual.lexema
            self._avancar()
            direita = self._analisar_expressao_aritmetica()
            return ExpressaoBinaria(esquerda, operador, direita)
        
        return esquerda

    def _analisar_expressao_aritmetica(self) -> Expressao:
        """
        Analisa expressão aritmética de adição/subtração
        expr_aritmetica -> termo ((+ | -) termo)*
        """
        esquerda = self._analisar_termo()
        
        while self.token_atual.tipo in {TipoToken.MAIS, TipoToken.MENOS}:
            operador = self.token_atual.lexema
            self._avancar()
            direita = self._analisar_termo()
            esquerda = ExpressaoBinaria(esquerda, operador, direita)
        
        return esquerda

    def _analisar_termo(self) -> Expressao:
        """
        Analisa termo aritmético de multiplicação/divisão/módulo
        termo -> potencia ((* | / | %) potencia)*
        """
        esquerda = self._analisar_potencia()

        while self.token_atual.tipo in {TipoToken.MULTIPLICACAO, TipoToken.DIVISAO, TipoToken.MODULO}:
            operador = self.token_atual.lexema
            self._avancar()
            direita = self._analisar_potencia()
            esquerda = ExpressaoBinaria(esquerda, operador, direita)

        return esquerda

    def _analisar_potencia(self) -> Expressao:
        """
        Analisa potenciação (associativa à direita)
        potencia -> fator (^ fator)*
        """
        esquerda = self._analisar_fator()

        if self.token_atual.tipo == TipoToken.POTENCIA:
            operador = self.token_atual.lexema
            self._avancar()
            # Associatividade à direita: recursão
            direita = self._analisar_potencia()
            return ExpressaoBinaria(esquerda, operador, direita)

        return esquerda

    def _analisar_fator(self) -> Expressao:
        """
        Analisa fator (elemento mais básico da expressão)
        fator -> numero | identificador | (expressao) | verdadeiro | falso | -fator
        """
        # Números
        if self.token_atual.tipo in {TipoToken.NUMERO_INTEIRO, TipoToken.NUMERO_REAL}:
            valor = self.token_atual.lexema
            linha, coluna = self.token_atual.linha, self.token_atual.coluna
            self._avancar()
            lit = Literal(valor)
            lit.linha = linha
            lit.coluna = coluna
            return lit
        
        # Literais booleanos
        if self.token_atual.tipo in {TipoToken.VERDADEIRO, TipoToken.FALSO}:
            valor = self.token_atual.lexema
            linha, coluna = self.token_atual.linha, self.token_atual.coluna
            self._avancar()
            lit = Literal(valor)
            lit.linha = linha
            lit.coluna = coluna
            return lit
        
        # Strings
        if self.token_atual.tipo == TipoToken.TEXTO:
            valor = self.token_atual.lexema
            linha, coluna = self.token_atual.linha, self.token_atual.coluna
            self._avancar()
            lit = Literal(f'"{valor}"')
            lit.linha = linha
            lit.coluna = coluna
            return lit
        
        # Variáveis
        if self.token_atual.tipo == TipoToken.IDENTIFICADOR:
            nome = self.token_atual.lexema
            linha, coluna = self.token_atual.linha, self.token_atual.coluna
            self._avancar()
            var = Variavel(nome)
            var.linha = linha
            var.coluna = coluna
            return var
        
        # Expressão entre parênteses
        if self.token_atual.tipo == TipoToken.ABRE_PARENTESES:
            self._avancar()
            expr = self._analisar_expressao()
            self._esperar_token(TipoToken.FECHA_PARENTESES)
            return expr
        
        # Expressão unária negativa
        if self.token_atual.tipo == TipoToken.MENOS:
            operador = self.token_atual.lexema
            linha, coluna = self.token_atual.linha, self.token_atual.coluna
            self._avancar()
            operando = self._analisar_fator()
            expr_un = ExpressaoUnaria(operador, operando)
            expr_un.linha = linha
            expr_un.coluna = coluna
            return expr_un
        
        # Token inesperado
        raise ErroSintatico(
            f"Expressão inesperada '{self.token_atual.lexema}'",
            self.token_atual.linha,
            self.token_atual.coluna
        )