"""
Otimizador de Código Intermediário

Este módulo implementa otimizações clássicas sobre o código intermediário
de 3 endereços, melhorando desempenho e reduzindo tamanho do código final.

OTIMIZAÇÕES IMPLEMENTADAS:
===========================

1. CONSTANT FOLDING (Dobramento de Constantes)
   - Avalia operações com constantes em tempo de compilação
   - Exemplo: x = 3 + 5  →  x = 8

2. CONSTANT PROPAGATION (Propagação de Constantes)
   - Substitui variáveis por seus valores constantes conhecidos
   - Exemplo: x = 5; y = x + 3  →  y = 5 + 3  →  y = 8

3. ALGEBRAIC SIMPLIFICATION (Simplificação Algébrica)
   - Aplica identidades matemáticas
   - Exemplos:
     * x + 0 → x
     * x * 1 → x
     * x * 0 → 0
     * x - 0 → x

4. DEAD CODE ELIMINATION (Eliminação de Código Morto)
   - Remove variáveis temporárias não utilizadas
   - Remove código após goto incondicional

5. COPY PROPAGATION (Propagação de Cópias)
   - Substitui cópias simples (x = y) pelo original
   - Exemplo: x = y; z = x + 1  →  z = y + 1

TEORIA:
=======
Otimizações de compiladores são transformações que preservam a
semântica do programa, mas melhoram:
- Tempo de execução
- Uso de memória
- Tamanho do código

As otimizações podem ser:
- Locais: dentro de um bloco básico
- Globais: entre blocos básicos
- Interprocedurais: entre funções
"""

from typing import List, Dict, Set, Optional
from copy import deepcopy
from .intermediate import InstrucaoIntermediaria


class OtimizadorCodigoIntermediario:
    """
    Otimiza código intermediário de 3 endereços
    
    Aplica múltiplas passadas de otimização até não haver mais mudanças.
    """
    
    def __init__(self):
        self.constantes: Dict[str, str] = {}  # Variável → valor constante
        self.copias: Dict[str, str] = {}      # Variável → variável copiada
        self.variaveis_usadas: Set[str] = set()
        self.modificacoes_feitas = False
        self.debug_pro = False

    def __init__(self, debug_pro: bool = False):
        self.constantes: Dict[str, str] = {}  # Variável → valor constante
        self.copias: Dict[str, str] = {}      # Variável → variável copiada
        self.variaveis_usadas: Set[str] = set()
        self.modificacoes_feitas = False
        self.debug_pro = debug_pro
    
    def otimizar(self, instrucoes: List[InstrucaoIntermediaria], 
                 max_passadas: int = 5) -> List[InstrucaoIntermediaria]:
        """
        Otimiza código intermediário com múltiplas passadas
        
        Args:
            instrucoes: Lista de instruções intermediárias
            max_passadas: Número máximo de passadas de otimização
            
        Returns:
            List[InstrucaoIntermediaria]: Código otimizado
        """
        codigo = deepcopy(instrucoes)
        
        for passada in range(max_passadas):
            self.modificacoes_feitas = False
            if self.debug_pro:
                print(f"[OPT] pass {passada+1} início")
            
            # Análise de variáveis usadas
            self._analisar_uso_variaveis(codigo)
            
            # Aplicar otimizações
            codigo = self._constant_folding(codigo)
            codigo = self._constant_propagation(codigo)
            codigo = self._algebraic_simplification(codigo)
            codigo = self._copy_propagation(codigo)
            codigo = self._dead_code_elimination(codigo)
            
            # Se não houve mudanças, parar
            if self.debug_pro:
                print(f"[OPT] pass {passada+1} modificacoes_feitas={self.modificacoes_feitas}")
            if not self.modificacoes_feitas:
                break

        if self.debug_pro:
            print(f"[OPT] otimização concluída após {passada+1} passadas")
        
        return codigo
    
    def _analisar_uso_variaveis(self, instrucoes: List[InstrucaoIntermediaria]) -> None:
        """Identifica quais variáveis são usadas no código"""
        self.variaveis_usadas = set()
        
        for instr in instrucoes:
            # Variáveis usadas no lado direito
            if instr.operando1 and not self._eh_constante(instr.operando1):
                self.variaveis_usadas.add(instr.operando1)
            if instr.operando2 and not self._eh_constante(instr.operando2):
                self.variaveis_usadas.add(instr.operando2)
            
            # Variáveis usadas em condicionais e escritas
            if instr.tipo in {'IFFALSE', 'IF', 'WRITE'}:
                if instr.operando1 and not self._eh_constante(instr.operando1):
                    self.variaveis_usadas.add(instr.operando1)
            
            # Variáveis não-temporárias sempre são consideradas usadas
            if instr.resultado and not instr.resultado.startswith('t'):
                self.variaveis_usadas.add(instr.resultado)
    
    def _constant_folding(self, instrucoes: List[InstrucaoIntermediaria]) \
            -> List[InstrucaoIntermediaria]:
        """
        Dobramento de constantes: avalia operações com constantes
        
        Exemplo:
            t1 = 3 + 5  →  t1 = 8
        """
        novas_instrucoes = []
        
        for instr in instrucoes:
            if instr.tipo == 'OP' and instr.operando2:
                # Verificar se ambos operandos são constantes
                if self._eh_constante(instr.operando1) and self._eh_constante(instr.operando2):
                    try:
                        resultado = self._avaliar_operacao(
                            instr.operando1,
                            instr.operador,
                            instr.operando2
                        )
                        
                        # Substituir por atribuição de constante
                        nova_instr = InstrucaoIntermediaria(
                            tipo='ASSIGN',
                            resultado=instr.resultado,
                            operando1=str(resultado)
                        )
                        novas_instrucoes.append(nova_instr)
                        self.modificacoes_feitas = True
                        continue
                    except:
                        pass  # Se falhar, manter instrução original
            
            novas_instrucoes.append(instr)
        
        return novas_instrucoes
    
    def _constant_propagation(self, instrucoes: List[InstrucaoIntermediaria]) \
            -> List[InstrucaoIntermediaria]:
        """
        Propagação de constantes: substitui variáveis por valores conhecidos
        
        Exemplo:
            x = 5
            y = x + 3  →  y = 5 + 3
        """
        constantes_locais = {}
        novas_instrucoes = []
        
        for instr in instrucoes:
            # Atualizar tabela de constantes
            if instr.tipo == 'ASSIGN' and self._eh_constante(instr.operando1):
                constantes_locais[instr.resultado] = instr.operando1
            elif instr.tipo in {'OP', 'UNARY', 'READ'}:
                # Variável deixa de ser constante
                if instr.resultado in constantes_locais:
                    del constantes_locais[instr.resultado]
            
            # Substituir variáveis por constantes conhecidas
            nova_instr = deepcopy(instr)
            
            if instr.operando1 in constantes_locais:
                nova_instr.operando1 = constantes_locais[instr.operando1]
                self.modificacoes_feitas = True
            
            if instr.operando2 and instr.operando2 in constantes_locais:
                nova_instr.operando2 = constantes_locais[instr.operando2]
                self.modificacoes_feitas = True
            
            novas_instrucoes.append(nova_instr)
        
        return novas_instrucoes
    
    def _algebraic_simplification(self, instrucoes: List[InstrucaoIntermediaria]) \
            -> List[InstrucaoIntermediaria]:
        """
        Simplificação algébrica: aplica identidades matemáticas
        
        Exemplos:
            x = y + 0  →  x = y
            x = y * 1  →  x = y
            x = y * 0  →  x = 0
        """
        novas_instrucoes = []
        
        for instr in instrucoes:
            if instr.tipo == 'OP' and instr.operando2:
                op1, op, op2 = instr.operando1, instr.operador, instr.operando2
                
                # x + 0 = x  ou  0 + x = x
                if op == '+' and (op2 == '0' or op1 == '0'):
                    operando = op1 if op2 == '0' else op2
                    novas_instrucoes.append(InstrucaoIntermediaria(
                        tipo='ASSIGN',
                        resultado=instr.resultado,
                        operando1=operando
                    ))
                    self.modificacoes_feitas = True
                    continue
                
                # x - 0 = x
                elif op == '-' and op2 == '0':
                    novas_instrucoes.append(InstrucaoIntermediaria(
                        tipo='ASSIGN',
                        resultado=instr.resultado,
                        operando1=op1
                    ))
                    self.modificacoes_feitas = True
                    continue
                
                # x * 1 = x  ou  1 * x = x
                elif op == '*' and (op2 == '1' or op1 == '1'):
                    operando = op1 if op2 == '1' else op2
                    novas_instrucoes.append(InstrucaoIntermediaria(
                        tipo='ASSIGN',
                        resultado=instr.resultado,
                        operando1=operando
                    ))
                    self.modificacoes_feitas = True
                    continue
                
                # x * 0 = 0  ou  0 * x = 0
                elif op == '*' and (op2 == '0' or op1 == '0'):
                    novas_instrucoes.append(InstrucaoIntermediaria(
                        tipo='ASSIGN',
                        resultado=instr.resultado,
                        operando1='0'
                    ))
                    self.modificacoes_feitas = True
                    continue
                
                # x / 1 = x
                elif op == '/' and op2 == '1':
                    novas_instrucoes.append(InstrucaoIntermediaria(
                        tipo='ASSIGN',
                        resultado=instr.resultado,
                        operando1=op1
                    ))
                    self.modificacoes_feitas = True
                    continue
            
            novas_instrucoes.append(instr)
        
        return novas_instrucoes
    
    def _copy_propagation(self, instrucoes: List[InstrucaoIntermediaria]) \
            -> List[InstrucaoIntermediaria]:
        """
        Propagação de cópias: substitui x por y se x = y
        
        Exemplo:
            x = y
            z = x + 1  →  z = y + 1
        """
        copias_locais = {}
        novas_instrucoes = []
        
        for instr in instrucoes:
            # Detectar cópias simples
            if (instr.tipo == 'ASSIGN' and 
                not self._eh_constante(instr.operando1) and
                instr.operando1):
                copias_locais[instr.resultado] = instr.operando1
            elif instr.tipo in {'OP', 'UNARY', 'READ'}:
                # Variável deixa de ser cópia
                if instr.resultado in copias_locais:
                    del copias_locais[instr.resultado]
            
            # Substituir usos de cópias
            nova_instr = deepcopy(instr)
            
            if instr.operando1 in copias_locais:
                nova_instr.operando1 = copias_locais[instr.operando1]
                self.modificacoes_feitas = True
            
            if instr.operando2 and instr.operando2 in copias_locais:
                nova_instr.operando2 = copias_locais[instr.operando2]
                self.modificacoes_feitas = True
            
            novas_instrucoes.append(nova_instr)
        
        return novas_instrucoes
    
    def _dead_code_elimination(self, instrucoes: List[InstrucaoIntermediaria]) \
            -> List[InstrucaoIntermediaria]:
        """
        Eliminação de código morto: remove instruções não utilizadas
        
        Remove:
        - Atribuições a temporários nunca usados
        - Código após goto incondicional
        """
        novas_instrucoes = []
        codigo_morto_ativo = False
        
        for instr in instrucoes:
            # Código após GOTO incondicional é morto (até próximo label)
            if instr.tipo == 'GOTO':
                novas_instrucoes.append(instr)
                codigo_morto_ativo = True
                continue
            
            # Label reativa código
            if instr.tipo == 'LABEL':
                codigo_morto_ativo = False
                novas_instrucoes.append(instr)
                continue
            
            # Pular código morto
            if codigo_morto_ativo:
                self.modificacoes_feitas = True
                continue
            
            # Remover atribuições a temporários não usados
            if (instr.tipo in {'ASSIGN', 'OP', 'UNARY'} and
                instr.resultado.startswith('t') and
                instr.resultado not in self.variaveis_usadas):
                self.modificacoes_feitas = True
                continue
            
            novas_instrucoes.append(instr)
        
        return novas_instrucoes
    
    def _eh_constante(self, valor: str) -> bool:
        """Verifica se um valor é uma constante"""
        if not valor:
            return False
        
        # Booleanos
        if valor in {'true', 'false'}:
            return True
        
        # Strings
        if valor.startswith('"') and valor.endswith('"'):
            return True
        
        # Números
        try:
            float(valor)
            return True
        except ValueError:
            return False
    
    def _avaliar_operacao(self, op1: str, operador: str, op2: str) -> str:
        """
        Avalia operação aritmética com constantes
        
        Args:
            op1: Operando esquerdo
            operador: Operador
            op2: Operando direito
            
        Returns:
            str: Resultado da operação
        """
        # Converter para números
        val1 = float(op1)
        val2 = float(op2)
        
        # Avaliar operação
        if operador == '+':
            resultado = val1 + val2
        elif operador == '-':
            resultado = val1 - val2
        elif operador == '*':
            resultado = val1 * val2
        elif operador == '/':
            resultado = val1 / val2
        elif operador == '%':
            resultado = val1 % val2
        elif operador == '^':
            resultado = val1 ** val2
        elif operador == '<':
            return 'true' if val1 < val2 else 'false'
        elif operador == '<=':
            return 'true' if val1 <= val2 else 'false'
        elif operador == '>':
            return 'true' if val1 > val2 else 'false'
        elif operador == '>=':
            return 'true' if val1 >= val2 else 'false'
        elif operador == '==':
            return 'true' if val1 == val2 else 'false'
        elif operador == '!=':
            return 'true' if val1 != val2 else 'false'
        else:
            raise ValueError(f"Operador '{operador}' não reconhecido")
        
        # Retornar inteiro se possível
        if isinstance(resultado, float) and resultado.is_integer():
            return str(int(resultado))
        return str(resultado)
    
    def relatorio_otimizacoes(self, original: List[InstrucaoIntermediaria],
                              otimizado: List[InstrucaoIntermediaria]) -> str:
        """
        Gera relatório comparativo das otimizações
        
        Args:
            original: Código original
            otimizado: Código otimizado
            
        Returns:
            str: Relatório formatado
        """
        linhas = [
            "=" * 70,
            "RELATÓRIO DE OTIMIZAÇÕES",
            "=" * 70,
            "",
            f"Instruções originais:  {len(original)}",
            f"Instruções otimizadas: {len(otimizado)}",
            f"Redução:               {len(original) - len(otimizado)} instruções " +
            f"({(len(original) - len(otimizado)) / len(original) * 100:.1f}%)",
            "",
            "OTIMIZAÇÕES APLICADAS:",
            "- Constant Folding (dobramento de constantes)",
            "- Constant Propagation (propagação de constantes)",
            "- Algebraic Simplification (simplificação algébrica)",
            "- Copy Propagation (propagação de cópias)",
            "- Dead Code Elimination (eliminação de código morto)",
            "",
            "=" * 70
        ]
        
        return '\n'.join(linhas)
