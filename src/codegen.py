"""
Gerador de Código para a linguagem Portugol

Este módulo implementa a geração de código Python a partir da AST,
convertendo construções Portugol para código Python equivalente.
"""

from typing import List, Dict
from .ast_nodes import (
    Programa, DeclaracaoVariavel, 
    Comando, Atribuicao, Condicional, Repeticao, Entrada, Saida,
    Expressao, ExpressaoBinaria, ExpressaoUnaria, Literal, Variavel
)


class GeradorDeCodigo:
    """
    Gerador de código Python a partir da AST Portugol
    
    Converte cada nó da AST em código Python equivalente,
    mantendo a semântica original do programa Portugol.
    """
    
    def __init__(self):
        self.codigo_gerado = []
        self.nivel_indentacao = 0
        self.mapeamento_tipos = {
            'inteiro': 'int',
            'real': 'float', 
            'caracter': 'str',
            'logico': 'bool'
        }
        self.tabela_tipos = {}  # Para armazenar tipos das variáveis

    def gerar(self, programa: Programa) -> str:
        """
        Gera código Python para o programa completo
        
        Args:
            programa: Nó raiz da AST
            
        Returns:
            str: Código Python gerado
        """
        self.codigo_gerado = []
        self.nivel_indentacao = 0
        
        # Cabeçalho do programa
        self._adicionar_linha("# Código gerado automaticamente do Portugol")
        self._adicionar_linha("")
        
        # Função principal
        self._adicionar_linha("def main():")
        self._aumentar_indentacao()
        
        # Declarações de variáveis (inicializadas com valores padrão)
        self._gerar_declaracoes(programa.declaracoes)
        
        # Comandos do programa
        if programa.comandos:
            for comando in programa.comandos:
                self._gerar_comando(comando)
        else:
            self._adicionar_linha("pass")
        
        self._diminuir_indentacao()
        self._adicionar_linha("")
        
        # Chamada da função principal
        self._adicionar_linha("if __name__ == '__main__':")
        self._adicionar_linha("    main()")
        
        return '\n'.join(self.codigo_gerado)

    def _gerar_declaracoes(self, declaracoes: List[DeclaracaoVariavel]) -> None:
        """Gera declarações de variáveis com valores padrão"""
        if declaracoes:
            self._adicionar_linha("# Declarações de variáveis")
            
        valores_padrao = {
            'inteiro': '0',
            'real': '0.0',
            'caracter': '""',
            'logico': 'False'
        }
        
        for declaracao in declaracoes:
            # Armazenar tipo da variável para uso posterior
            self.tabela_tipos[declaracao.nome] = declaracao.tipo
            
            valor_padrao = valores_padrao.get(declaracao.tipo, 'None')
            self._adicionar_linha(f"{declaracao.nome} = {valor_padrao}")
        
        if declaracoes:
            self._adicionar_linha("")

    def _gerar_comando(self, comando: Comando) -> None:
        """Gera código para um comando"""
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
        """Gera código para atribuição"""
        expressao_codigo = self._gerar_expressao(atribuicao.expressao)
        self._adicionar_linha(f"{atribuicao.variavel} = {expressao_codigo}")

    def _gerar_condicional(self, condicional: Condicional) -> None:
        """Gera código para estrutura condicional"""
        condicao_codigo = self._gerar_expressao(condicional.condicao)
        self._adicionar_linha(f"if {condicao_codigo}:")
        
        self._aumentar_indentacao()
        if condicional.comandos_entao:
            for comando in condicional.comandos_entao:
                self._gerar_comando(comando)
        else:
            self._adicionar_linha("pass")
        self._diminuir_indentacao()
        
        if condicional.comandos_senao:
            self._adicionar_linha("else:")
            self._aumentar_indentacao()
            for comando in condicional.comandos_senao:
                self._gerar_comando(comando)
            self._diminuir_indentacao()

    def _gerar_repeticao(self, repeticao: Repeticao) -> None:
        """Gera código para estrutura de repetição"""
        condicao_codigo = self._gerar_expressao(repeticao.condicao)
        self._adicionar_linha(f"while {condicao_codigo}:")
        
        self._aumentar_indentacao()
        if repeticao.comandos:
            for comando in repeticao.comandos:
                self._gerar_comando(comando)
        else:
            self._adicionar_linha("pass")
        self._diminuir_indentacao()

    def _gerar_entrada(self, entrada: Entrada) -> None:
        """Gera código para comando de entrada"""
        # Conversão automática de tipo baseada na declaração da variável
        tipo_variavel = self.tabela_tipos.get(entrada.variavel, 'caracter')
        
        if tipo_variavel == 'inteiro':
            # Conversão inline com tratamento de erro em uma linha
            self._adicionar_linha(f'_input_temp = input("Digite um valor: ")')
            self._adicionar_linha(f'try:')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = int(_input_temp)')
            self._diminuir_indentacao()
            self._adicionar_linha(f'except (ValueError, EOFError):')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = 0  # Valor padrão para entrada inválida')
            self._diminuir_indentacao()
            
        elif tipo_variavel == 'real':
            # Conversão inline com tratamento de erro em uma linha
            self._adicionar_linha(f'_input_temp = input("Digite um valor: ")')
            self._adicionar_linha(f'try:')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = float(_input_temp)')
            self._diminuir_indentacao()
            self._adicionar_linha(f'except (ValueError, EOFError):')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = 0.0  # Valor padrão para entrada inválida')
            self._diminuir_indentacao()
            
        elif tipo_variavel == 'logico':
            self._adicionar_linha(f'try:')
            self._aumentar_indentacao()
            self._adicionar_linha(f'_input_temp = input("Digite um valor: ")')
            self._adicionar_linha(f"{entrada.variavel} = _input_temp.lower() in ['true', 'verdadeiro', '1', 'sim', 's']")
            self._diminuir_indentacao()
            self._adicionar_linha(f'except EOFError:')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = False  # Valor padrão para entrada inválida')
            self._diminuir_indentacao()
        else:
            # Para 'caracter', mantém como string
            self._adicionar_linha(f'try:')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = input("Digite um valor: ")')
            self._diminuir_indentacao()
            self._adicionar_linha(f'except EOFError:')
            self._aumentar_indentacao()
            self._adicionar_linha(f'{entrada.variavel} = ""  # Valor padrão para entrada inválida')
            self._diminuir_indentacao()

    def _gerar_saida(self, saida: Saida) -> None:
        """Gera código para comando de saída"""
        expressoes_codigo = []
        for expressao in saida.expressoes:
            expressoes_codigo.append(self._gerar_expressao(expressao))
        
        # Usar vírgulas para separar as expressões no print
        codigo_print = ", ".join(expressoes_codigo)
        self._adicionar_linha(f"print({codigo_print})")

    def _gerar_expressao(self, expressao: Expressao) -> str:
        """
        Gera código para uma expressão
        
        Args:
            expressao: Nó da expressão
            
        Returns:
            str: Código Python da expressão
        """
        if isinstance(expressao, Literal):
            return self._gerar_literal(expressao)
        elif isinstance(expressao, Variavel):
            return expressao.nome
        elif isinstance(expressao, ExpressaoBinaria):
            return self._gerar_expressao_binaria(expressao)
        elif isinstance(expressao, ExpressaoUnaria):
            return self._gerar_expressao_unaria(expressao)
        else:
            return "# Expressão não reconhecida"

    def _gerar_literal(self, literal: Literal) -> str:
        """Gera código para literal"""
        valor = literal.valor
        
        # Booleanos Portugol -> Python
        if valor == 'verdadeiro':
            return 'True'
        elif valor == 'falso':
            return 'False'
        
        # Strings já vêm com aspas
        if valor.startswith('"') and valor.endswith('"'):
            return valor
        
        # Números e outros valores literais
        return valor

    def _gerar_expressao_binaria(self, expressao: ExpressaoBinaria) -> str:
        """Gera código para expressão binária"""
        esquerda = self._gerar_expressao(expressao.esquerda)
        direita = self._gerar_expressao(expressao.direita)
        operador = expressao.operador
        
        # Mapeamento de operadores Portugol -> Python
        mapeamento_operadores = {
            'e': 'and',
            'ou': 'or',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '<=': '<=',
            '>': '>',
            '>=': '>=',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/'
        }
        
        operador_python = mapeamento_operadores.get(operador, operador)
        return f"({esquerda} {operador_python} {direita})"

    def _gerar_expressao_unaria(self, expressao: ExpressaoUnaria) -> str:
        """Gera código para expressão unária"""
        operando = self._gerar_expressao(expressao.operando)
        operador = expressao.operador
        
        if operador == '-':
            return f"(-{operando})"
        else:
            return f"({operador}{operando})"

    def _adicionar_linha(self, linha: str) -> None:
        """Adiciona uma linha de código com indentação apropriada"""
        indentacao = "    " * self.nivel_indentacao
        self.codigo_gerado.append(indentacao + linha)

    def _aumentar_indentacao(self) -> None:
        """Aumenta o nível de indentação"""
        self.nivel_indentacao += 1

    def _diminuir_indentacao(self) -> None:
        """Diminui o nível de indentação"""
        if self.nivel_indentacao > 0:
            self.nivel_indentacao -= 1