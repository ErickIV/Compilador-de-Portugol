"""
Gerador de Código Intermediário (Representação de 3 Endereços)

Este módulo implementa a geração de código intermediário a partir da AST,
produzindo uma representação linear de operações que facilita otimizações
e geração de código final.

TEORIA - CÓDIGO DE 3 ENDEREÇOS:
================================
Cada instrução tem no máximo 3 operandos:
    x = y op z

Tipos de instruções:
1. Atribuição: x = y
2. Aritmética: x = y op z (op: +, -, *, /)
3. Lógica: x = y op z (op: and, or, ==, !=, <, >, <=, >=)
4. Cópia: x = y
5. Unária: x = op y (op: -, not)
6. Saltos: goto L, if x goto L, ifFalse x goto L
7. E/S: read x, write x
8. Labels: L:

EXEMPLO:
========
Código Portugol:
    x <- 5 + 3 * 2

Código Intermediário:
    t1 = 3 * 2
    t2 = 5 + t1
    x = t2
"""

from typing import List, Union, Optional
from dataclasses import dataclass
from .ast_nodes import (
    Programa, DeclaracaoVariavel,
    Comando, Atribuicao, Condicional, Repeticao, Entrada, Saida,
    Expressao, ExpressaoBinaria, ExpressaoUnaria, Literal, Variavel
)


@dataclass
class InstrucaoIntermediaria:
    """
    Representa uma instrução de código intermediário de 3 endereços
    
    Atributos:
        tipo: Tipo da instrução (ASSIGN, OP, GOTO, LABEL, etc.)
        resultado: Operando destino (lado esquerdo)
        operando1: Primeiro operando (lado direito)
        operador: Operador (se aplicável)
        operando2: Segundo operando (se aplicável)
    """
    tipo: str
    resultado: Optional[str] = None
    operando1: Optional[str] = None
    operador: Optional[str] = None
    operando2: Optional[str] = None
    
    def __str__(self) -> str:
        """Representação textual da instrução"""
        if self.tipo == 'LABEL':
            return f"{self.resultado}:"
        elif self.tipo == 'ASSIGN':
            return f"{self.resultado} = {self.operando1}"
        elif self.tipo == 'OP' and self.operando2:
            return f"{self.resultado} = {self.operando1} {self.operador} {self.operando2}"
        elif self.tipo == 'UNARY':
            return f"{self.resultado} = {self.operador} {self.operando1}"
        elif self.tipo == 'GOTO':
            return f"goto {self.resultado}"
        elif self.tipo == 'IF':
            return f"if {self.operando1} goto {self.resultado}"
        elif self.tipo == 'IFFALSE':
            return f"ifFalse {self.operando1} goto {self.resultado}"
        elif self.tipo == 'READ':
            return f"read {self.resultado}"
        elif self.tipo == 'WRITE':
            return f"write {self.operando1}"
        elif self.tipo == 'INIT':
            return f"{self.resultado} = {self.operando1}  // inicialização"
        else:
            return f"// instrução desconhecida: {self.tipo}"


class GeradorCodigoIntermediario:
    """
    Gera código intermediário de 3 endereços a partir da AST
    
    Mantém:
    - Lista de instruções geradas
    - Contador de temporários (t1, t2, t3, ...)
    - Contador de labels (L1, L2, L3, ...)
    """
    
    def __init__(self):
        self.instrucoes: List[InstrucaoIntermediaria] = []
        self.contador_temporarios = 0
        self.contador_labels = 0
    
    def novo_temporario(self) -> str:
        """Gera um novo nome de variável temporária"""
        self.contador_temporarios += 1
        return f"t{self.contador_temporarios}"
    
    def novo_label(self) -> str:
        """Gera um novo nome de label"""
        self.contador_labels += 1
        return f"L{self.contador_labels}"
    
    def adicionar_instrucao(self, instrucao: InstrucaoIntermediaria) -> None:
        """Adiciona uma instrução à lista"""
        self.instrucoes.append(instrucao)
    
    def gerar(self, programa: Programa) -> List[InstrucaoIntermediaria]:
        """
        Gera código intermediário para o programa completo
        
        Args:
            programa: Nó raiz da AST
            
        Returns:
            List[InstrucaoIntermediaria]: Lista de instruções intermediárias
        """
        self.instrucoes = []
        self.contador_temporarios = 0
        self.contador_labels = 0
        
        # Inicializar variáveis declaradas
        for declaracao in programa.declaracoes:
            self._gerar_declaracao(declaracao)
        
        # Gerar código para comandos
        for comando in programa.comandos:
            self._gerar_comando(comando)
        
        return self.instrucoes
    
    def _gerar_declaracao(self, declaracao: DeclaracaoVariavel) -> None:
        """Gera inicialização de variável"""
        valores_padrao = {
            'inteiro': '0',
            'real': '0.0',
            'caracter': '""',
            'logico': 'false'
        }
        
        valor_inicial = valores_padrao.get(declaracao.tipo, '0')
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='INIT',
            resultado=declaracao.nome,
            operando1=valor_inicial
        ))
    
    def _gerar_comando(self, comando: Comando) -> None:
        """Gera código intermediário para um comando"""
        if isinstance(comando, Atribuicao):
            self._gerar_atribuicao(comando)
        elif isinstance(comando, Condicional):
            self._gerar_condicional(comando)
        elif isinstance(comando, Repeticao):
            self._gerar_repeticao(comando)
        elif isinstance(comando, Entrada):
            self._gerar_entrada(comando)
        elif isinstance(comando, Saida):
            self._gerar_saida(comando)
    
    def _gerar_atribuicao(self, atribuicao: Atribuicao) -> None:
        """
        Gera código intermediário para atribuição
        
        Exemplo:
            x <- a + b * c
        
        Gera:
            t1 = b * c
            t2 = a + t1
            x = t2
        """
        # Gerar código para expressão (retorna temporário ou variável)
        temp_expr = self._gerar_expressao(atribuicao.expressao)
        
        # Atribuir resultado à variável
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='ASSIGN',
            resultado=atribuicao.variavel,
            operando1=temp_expr
        ))
    
    def _gerar_condicional(self, condicional: Condicional) -> None:
        """
        Gera código intermediário para estrutura condicional
        
        Estrutura:
            ifFalse condicao goto L_senao
            [comandos_entao]
            goto L_fim
        L_senao:
            [comandos_senao]
        L_fim:
        """
        # Avaliar condição
        temp_condicao = self._gerar_expressao(condicional.condicao)
        
        label_senao = self.novo_label()
        label_fim = self.novo_label()
        
        # Se condição falsa, pular para senão (ou fim)
        if condicional.comandos_senao:
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='IFFALSE',
                resultado=label_senao,
                operando1=temp_condicao
            ))
        else:
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='IFFALSE',
                resultado=label_fim,
                operando1=temp_condicao
            ))
        
        # Comandos do "então"
        for comando in condicional.comandos_entao:
            self._gerar_comando(comando)
        
        # Se há senão, pular para fim após executar então
        if condicional.comandos_senao:
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='GOTO',
                resultado=label_fim
            ))
            
            # Label do senão
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='LABEL',
                resultado=label_senao
            ))
            
            # Comandos do "senão"
            for comando in condicional.comandos_senao:
                self._gerar_comando(comando)
        
        # Label do fim
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='LABEL',
            resultado=label_fim
        ))
    
    def _gerar_repeticao(self, repeticao: Repeticao) -> None:
        """
        Gera código intermediário para loop while
        
        Estrutura:
        L_inicio:
            ifFalse condicao goto L_fim
            [comandos]
            goto L_inicio
        L_fim:
        """
        label_inicio = self.novo_label()
        label_fim = self.novo_label()
        
        # Label do início do loop
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='LABEL',
            resultado=label_inicio
        ))
        
        # Avaliar condição
        temp_condicao = self._gerar_expressao(repeticao.condicao)
        
        # Se falso, sair do loop
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='IFFALSE',
            resultado=label_fim,
            operando1=temp_condicao
        ))
        
        # Comandos do loop
        for comando in repeticao.comandos:
            self._gerar_comando(comando)
        
        # Voltar para início
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='GOTO',
            resultado=label_inicio
        ))
        
        # Label do fim
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='LABEL',
            resultado=label_fim
        ))
    
    def _gerar_entrada(self, entrada: Entrada) -> None:
        """Gera instrução de leitura"""
        self.adicionar_instrucao(InstrucaoIntermediaria(
            tipo='READ',
            resultado=entrada.variavel
        ))
    
    def _gerar_saida(self, saida: Saida) -> None:
        """Gera instruções de escrita"""
        for expressao in saida.expressoes:
            temp = self._gerar_expressao(expressao)
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='WRITE',
                operando1=temp
            ))
    
    def _gerar_expressao(self, expressao: Expressao) -> str:
        """
        Gera código intermediário para uma expressão
        
        Args:
            expressao: Nó da expressão
            
        Returns:
            str: Nome do temporário ou variável que contém o resultado
        """
        if isinstance(expressao, Literal):
            # Literais são usados diretamente
            valor = expressao.valor
            if valor == 'verdadeiro':
                return 'true'
            elif valor == 'falso':
                return 'false'
            return valor
        
        elif isinstance(expressao, Variavel):
            # Variáveis são usadas diretamente
            return expressao.nome
        
        elif isinstance(expressao, ExpressaoBinaria):
            # Avaliar operandos
            temp1 = self._gerar_expressao(expressao.esquerda)
            temp2 = self._gerar_expressao(expressao.direita)
            
            # Criar temporário para resultado
            resultado = self.novo_temporario()
            
            # Mapear operadores Portugol → intermediário
            operador = expressao.operador
            if operador == 'e':
                operador = 'and'
            elif operador == 'ou':
                operador = 'or'
            
            # Adicionar instrução
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='OP',
                resultado=resultado,
                operando1=temp1,
                operador=operador,
                operando2=temp2
            ))
            
            return resultado
        
        elif isinstance(expressao, ExpressaoUnaria):
            # Avaliar operando
            temp = self._gerar_expressao(expressao.operando)
            
            # Criar temporário para resultado
            resultado = self.novo_temporario()
            
            # Adicionar instrução unária
            self.adicionar_instrucao(InstrucaoIntermediaria(
                tipo='UNARY',
                resultado=resultado,
                operador=expressao.operador,
                operando1=temp
            ))
            
            return resultado
        
        else:
            # Expressão desconhecida
            return "???"
    
    def imprimir_codigo(self) -> str:
        """
        Retorna representação textual do código intermediário
        
        Returns:
            str: Código intermediário formatado
        """
        linhas = [
            "=" * 60,
            "CÓDIGO INTERMEDIÁRIO (3 ENDEREÇOS)",
            "=" * 60,
            ""
        ]
        
        for i, instrucao in enumerate(self.instrucoes, 1):
            linhas.append(f"{i:3d}. {str(instrucao)}")
        
        linhas.append("")
        linhas.append("=" * 60)
        
        return '\n'.join(linhas)
