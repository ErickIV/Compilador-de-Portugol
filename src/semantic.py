"""
Analisador Semântico para a linguagem Portugol

Este módulo implementa a análise semântica, verificando:
- Declaração e uso de variáveis
- Compatibilidade de tipos em operações
- Escopo e visibilidade
"""

from typing import Dict, Set, Any, Union
from .ast_nodes import (
    Programa, DeclaracaoVariavel,
    Comando, Atribuicao, Condicional, Repeticao, RepeticaoPara, Entrada, Saida,
    Expressao, ExpressaoBinaria, ExpressaoUnaria, Literal, Variavel
)
from .exceptions import ErroSemantico


class TabelaSimbolos:
    """
    Tabela de símbolos para rastrear variáveis declaradas
    
    Mantém informações sobre:
    - Nome da variável
    - Tipo declarado
    - Status de inicialização
    """
    
    def __init__(self):
        self.simbolos: Dict[str, Dict[str, Any]] = {}

    def declarar_variavel(self, nome: str, tipo: str, linha: int, coluna: int) -> None:
        """
        Declara uma nova variável na tabela de símbolos
        
        Args:
            nome: Nome da variável
            tipo: Tipo da variável (inteiro, real, caracter, logico)
            linha: Linha da declaração
            coluna: Coluna da declaração
            
        Raises:
            ErroSemantico: Se a variável já foi declarada
        """
        if nome in self.simbolos:
            raise ErroSemantico(
                f"Variável '{nome}' já foi declarada",
                linha, coluna
            )
        
        self.simbolos[nome] = {
            'tipo': tipo,
            'inicializada': False,
            'linha_declaracao': linha,
            'coluna_declaracao': coluna
        }

    def verificar_variavel_declarada(self, nome: str, linha: int, coluna: int) -> str:
        """
        Verifica se uma variável foi declarada
        
        Args:
            nome: Nome da variável
            linha: Linha do uso
            coluna: Coluna do uso
            
        Returns:
            str: Tipo da variável
            
        Raises:
            ErroSemantico: Se a variável não foi declarada
        """
        if nome not in self.simbolos:
            raise ErroSemantico(
                f"Variável '{nome}' não foi declarada",
                linha, coluna
            )
        
        return self.simbolos[nome]['tipo']

    def marcar_como_inicializada(self, nome: str) -> None:
        """Marca uma variável como inicializada"""
        if nome in self.simbolos:
            self.simbolos[nome]['inicializada'] = True

    def verificar_inicializada(self, nome: str, linha: int, coluna: int) -> None:
        """
        Verifica se uma variável foi inicializada antes do uso
        
        Emite um warning se a variável não foi inicializada.
        """
        if nome in self.simbolos and not self.simbolos[nome]['inicializada']:
            # Emitir warning ao invés de erro fatal
            import warnings
            warnings.warn(
                f"Variável '{nome}' pode estar sendo usada antes de ser inicializada " +
                f"(linha {linha}, coluna {coluna})",
                SyntaxWarning,
                stacklevel=2
            )

    def obter_tipo(self, nome: str) -> str:
        """Obtém o tipo de uma variável"""
        return self.simbolos.get(nome, {}).get('tipo', 'desconhecido')


class AnalisadorSemantico:
    """
    Analisador semântico para a linguagem Portugol
    
    Percorre a AST verificando:
    - Consistência de tipos
    - Declaração e uso de variáveis
    - Compatibilidade de operações
    """
    
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()
        self.tipos_compativel_int_real = {'inteiro', 'real'}

    def analisar(self, programa: Programa) -> None:
        """
        Analisa semanticamente o programa completo
        
        Args:
            programa: Nó raiz da AST
        """
        # Primeira passada: registrar todas as declarações
        for declaracao in programa.declaracoes:
            self._analisar_declaracao(declaracao)
        
        # Segunda passada: analisar comandos
        for comando in programa.comandos:
            self._analisar_comando(comando)

    def _analisar_declaracao(self, declaracao: DeclaracaoVariavel) -> None:
        """Analisa uma declaração de variável"""
        self.tabela_simbolos.declarar_variavel(
            declaracao.nome,
            declaracao.tipo,
            getattr(declaracao, 'linha', 0),
            getattr(declaracao, 'coluna', 0)
        )

    def _analisar_comando(self, comando: Comando) -> None:
        """Analisa um comando"""
        if isinstance(comando, Atribuicao):
            self._analisar_atribuicao(comando)
        elif isinstance(comando, Condicional):
            self._analisar_condicional(comando)
        elif isinstance(comando, Repeticao):
            self._analisar_repeticao(comando)
        elif isinstance(comando, RepeticaoPara):
            self._analisar_repeticao_para(comando)
        elif isinstance(comando, Entrada):
            self._analisar_entrada(comando)
        elif isinstance(comando, Saida):
            self._analisar_saida(comando)

    def _analisar_atribuicao(self, atribuicao: Atribuicao) -> None:
        """Analisa comando de atribuição"""
        # Verificar se variável foi declarada
        tipo_variavel = self.tabela_simbolos.verificar_variavel_declarada(
            atribuicao.variavel, 
            getattr(atribuicao, 'linha', 0), 
            getattr(atribuicao, 'coluna', 0)
        )
        
        # Analisar expressão do lado direito
        tipo_expressao = self._analisar_expressao(atribuicao.expressao)
        
        # Verificar compatibilidade de tipos
        self._verificar_compatibilidade_tipos(
            tipo_variavel, tipo_expressao, 
            getattr(atribuicao, 'linha', 0), 
            getattr(atribuicao, 'coluna', 0),
            f"Atribuição incompatível: '{tipo_variavel}' = '{tipo_expressao}'"
        )
        
        # Marcar variável como inicializada
        self.tabela_simbolos.marcar_como_inicializada(atribuicao.variavel)

    def _analisar_condicional(self, condicional: Condicional) -> None:
        """Analisa comando condicional"""
        # Analisar condição (deve ser lógica)
        tipo_condicao = self._analisar_expressao(condicional.condicao)
        if tipo_condicao != 'logico':
            # Permitir conversão implícita para booleano
            pass
        
        # Analisar comandos do 'então'
        for comando in condicional.comandos_entao:
            self._analisar_comando(comando)
        
        # Analisar comandos do 'senão' (se existir)
        for comando in condicional.comandos_senao:
            self._analisar_comando(comando)

    def _analisar_repeticao(self, repeticao: Repeticao) -> None:
        """Analisa comando de repetição"""
        # Analisar condição (deve ser lógica)
        tipo_condicao = self._analisar_expressao(repeticao.condicao)
        if tipo_condicao != 'logico':
            # Permitir conversão implícita para booleano
            pass

        # Analisar comandos do loop
        for comando in repeticao.comandos:
            self._analisar_comando(comando)

    def _analisar_repeticao_para(self, repeticao: RepeticaoPara) -> None:
        """Analisa comando de repetição 'para'"""
        # Verificar se variável foi declarada
        self.tabela_simbolos.verificar_variavel_declarada(
            repeticao.variavel,
            0, 0
        )

        # Analisar expressões de início, fim e passo
        self._analisar_expressao(repeticao.inicio)
        self._analisar_expressao(repeticao.fim)
        self._analisar_expressao(repeticao.passo)

        # Marcar variável como inicializada
        self.tabela_simbolos.marcar_como_inicializada(repeticao.variavel)

        # Analisar comandos do loop
        for comando in repeticao.comandos:
            self._analisar_comando(comando)

    def _analisar_entrada(self, entrada: Entrada) -> None:
        """Analisa comando de entrada"""
        # Verificar se variável foi declarada
        self.tabela_simbolos.verificar_variavel_declarada(
            entrada.variavel, 
            getattr(entrada, 'linha', 0), 
            getattr(entrada, 'coluna', 0)
        )
        
        # Marcar como inicializada
        self.tabela_simbolos.marcar_como_inicializada(entrada.variavel)

    def _analisar_saida(self, saida: Saida) -> None:
        """Analisa comando de saída"""
        # Analisar todas as expressões
        for expressao in saida.expressoes:
            self._analisar_expressao(expressao)

    def _analisar_expressao(self, expressao: Expressao) -> str:
        """
        Analisa uma expressão e retorna seu tipo
        
        Args:
            expressao: Nó da expressão
            
        Returns:
            str: Tipo da expressão
        """
        if isinstance(expressao, Literal):
            return self._inferir_tipo_literal(expressao.valor)
        
        elif isinstance(expressao, Variavel):
            # Verificar se variável foi declarada
            tipo = self.tabela_simbolos.verificar_variavel_declarada(
                expressao.nome, 
                getattr(expressao, 'linha', 0), 
                getattr(expressao, 'coluna', 0)
            )
            
            # Verificar se foi inicializada
            self.tabela_simbolos.verificar_inicializada(
                expressao.nome, 
                getattr(expressao, 'linha', 0), 
                getattr(expressao, 'coluna', 0)
            )
            
            return tipo
        
        elif isinstance(expressao, ExpressaoBinaria):
            return self._analisar_expressao_binaria(expressao)
        
        elif isinstance(expressao, ExpressaoUnaria):
            return self._analisar_expressao_unaria(expressao)
        
        else:
            raise ErroSemantico(f"Tipo de expressão não reconhecido", 0, 0)

    def _analisar_expressao_binaria(self, expressao: ExpressaoBinaria) -> str:
        """Analisa expressão binária e verifica compatibilidade de tipos"""
        tipo_esquerda = self._analisar_expressao(expressao.esquerda)
        tipo_direita = self._analisar_expressao(expressao.direita)
        operador = expressao.operador
        
        # Operadores aritméticos
        if operador in {'+', '-', '*', '%'}:
            if (tipo_esquerda in self.tipos_compativel_int_real and
                tipo_direita in self.tipos_compativel_int_real):
                # Se um dos operandos é real, resultado é real
                if tipo_esquerda == 'real' or tipo_direita == 'real':
                    return 'real'
                return 'inteiro'
            else:
                raise ErroSemantico(
                    f"Operação aritmética '{operador}' incompatível entre '{tipo_esquerda}' e '{tipo_direita}'",
                    0, 0
                )

        # Divisão e potenciação sempre retornam real (comportamento do Python 3)
        elif operador in {'/', '^'}:
            if (tipo_esquerda in self.tipos_compativel_int_real and
                tipo_direita in self.tipos_compativel_int_real):
                return 'real'  # Divisão e potenciação sempre retornam real
            else:
                raise ErroSemantico(
                    f"Operação aritmética '{operador}' incompatível entre '{tipo_esquerda}' e '{tipo_direita}'",
                    0, 0
                )
        
        # Operadores relacionais
        elif operador in {'==', '!=', '<', '<=', '>', '>='}:
            if (tipo_esquerda in self.tipos_compativel_int_real and 
                tipo_direita in self.tipos_compativel_int_real):
                return 'logico'
            elif tipo_esquerda == tipo_direita:
                return 'logico'
            else:
                # Permitir comparações flexíveis
                return 'logico'
        
        # Operadores lógicos
        elif operador in {'e', 'ou'}:
            # Operadores lógicos esperam operandos lógicos, mas permitem conversão
            return 'logico'
        
        else:
            raise ErroSemantico(f"Operador '{operador}' não reconhecido", 0, 0)

    def _analisar_expressao_unaria(self, expressao: ExpressaoUnaria) -> str:
        """Analisa expressão unária"""
        tipo_operando = self._analisar_expressao(expressao.operando)
        operador = expressao.operador
        
        if operador == '-':
            if tipo_operando in self.tipos_compativel_int_real:
                return tipo_operando
            else:
                raise ErroSemantico(
                    f"Operador unário '-' não aplicável a '{tipo_operando}'",
                    0, 0
                )
        
        else:
            raise ErroSemantico(f"Operador unário '{operador}' não reconhecido", 0, 0)

    def _inferir_tipo_literal(self, valor: str) -> str:
        """Infere o tipo de um literal baseado em seu valor"""
        # Remover aspas de strings
        if valor.startswith('"') and valor.endswith('"'):
            return 'caracter'
        
        # Booleanos
        if valor in {'verdadeiro', 'falso'}:
            return 'logico'
        
        # Números
        if '.' in valor:
            return 'real'
        
        # Verificar se é número inteiro
        try:
            int(valor)
            return 'inteiro'
        except ValueError:
            return 'caracter'  # Default para string

    def _verificar_compatibilidade_tipos(self, tipo1: str, tipo2: str, 
                                       linha: int, coluna: int, mensagem: str) -> None:
        """
        Verifica se dois tipos são compatíveis
        
        Args:
            tipo1: Primeiro tipo
            tipo2: Segundo tipo
            linha: Linha do erro
            coluna: Coluna do erro
            mensagem: Mensagem de erro
            
        Raises:
            ErroSemantico: Se os tipos não são compatíveis
        """
        if tipo1 == tipo2:
            return
        
        # Compatibilidade entre inteiro e real
        if (tipo1 in self.tipos_compativel_int_real and 
            tipo2 in self.tipos_compativel_int_real):
            return
        
        # Permitir tipos desconhecidos (pode ser literal ou erro anterior)
        if tipo1 == 'desconhecido' or tipo2 == 'desconhecido':
            return
        
        # Tipos incompatíveis - lançar erro
        raise ErroSemantico(mensagem, linha, coluna)