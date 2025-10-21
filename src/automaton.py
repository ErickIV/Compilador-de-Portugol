"""
Autômatos Finitos Determinísticos (AFD) para reconhecimento de tokens

Este módulo implementa AFDs explícitos para fins educacionais, demonstrando
como os padrões de tokens podem ser reconhecidos usando máquinas de estados finitos.

TEORIA:
=======
Um AFD é uma tupla (Q, Σ, δ, q0, F) onde:
- Q: Conjunto finito de estados
- Σ: Alfabeto de entrada (caracteres)
- δ: Função de transição (Q × Σ → Q)
- q0: Estado inicial
- F: Conjunto de estados finais (aceitação)

EXEMPLO - AFD para reconhecer identificadores:
Estados: {q0, q1, q_erro}
Alfabeto: {a-z, A-Z, 0-9, _}
Estado inicial: q0
Estados finais: {q1}

Transições:
- q0 --[a-zA-Z_]--> q1
- q1 --[a-zA-Z0-9_]--> q1
- qualquer outro → q_erro
"""

from typing import Dict, Set, Optional, Callable
from enum import Enum


class EstadoAFD(Enum):
    """Estados possíveis dos AFDs"""
    Q0 = "q0"  # Estado inicial
    Q1 = "q1"  # Estado intermediário/final
    Q2 = "q2"  # Estado para números reais (após o ponto)
    ERRO = "erro"  # Estado de erro


class AFD:
    """
    Classe base para Autômato Finito Determinístico
    
    Implementa a estrutura básica de um AFD com:
    - Tabela de transições
    - Estado atual
    - Verificação de estados finais
    """
    
    def __init__(self, estados_finais: Set[EstadoAFD]):
        """
        Inicializa o AFD
        
        Args:
            estados_finais: Conjunto de estados de aceitação
        """
        self.estado_atual = EstadoAFD.Q0
        self.estados_finais = estados_finais
        self.tabela_transicoes: Dict[EstadoAFD, Dict[str, EstadoAFD]] = {}
    
    def resetar(self) -> None:
        """Reseta o AFD para o estado inicial"""
        self.estado_atual = EstadoAFD.Q0
    
    def transitar(self, simbolo: str) -> bool:
        """
        Processa um símbolo e transita para o próximo estado
        
        Args:
            simbolo: Caractere de entrada
            
        Returns:
            bool: True se transição foi bem-sucedida, False se erro
        """
        if self.estado_atual not in self.tabela_transicoes:
            self.estado_atual = EstadoAFD.ERRO
            return False
        
        transicoes = self.tabela_transicoes[self.estado_atual]
        
        # Verificar transição direta
        if simbolo in transicoes:
            self.estado_atual = transicoes[simbolo]
            return True
        
        # Verificar transições por categoria (usando funções)
        for chave, proximo_estado in transicoes.items():
            if chave.startswith('_') and callable(getattr(self, chave, None)):
                predicado = getattr(self, chave)
                if predicado(simbolo):
                    self.estado_atual = proximo_estado
                    return True
        
        # Nenhuma transição encontrada
        self.estado_atual = EstadoAFD.ERRO
        return False
    
    def esta_em_estado_final(self) -> bool:
        """Verifica se o estado atual é um estado final"""
        return self.estado_atual in self.estados_finais
    
    def processar_string(self, entrada: str) -> bool:
        """
        Processa uma string completa
        
        Args:
            entrada: String a ser reconhecida
            
        Returns:
            bool: True se a string é aceita pelo AFD
        """
        self.resetar()
        
        for simbolo in entrada:
            if not self.transitar(simbolo):
                return False
        
        return self.esta_em_estado_final()


class AFDIdentificador(AFD):
    """
    AFD para reconhecer identificadores
    
    PADRÃO: [a-zA-Z_][a-zA-Z0-9_]*
    
    Estados:
    - q0: inicial
    - q1: final (viu pelo menos uma letra ou underscore)
    
    Transições:
    - q0 --[a-zA-Z_]--> q1
    - q1 --[a-zA-Z0-9_]--> q1
    """
    
    def __init__(self):
        super().__init__(estados_finais={EstadoAFD.Q1})
        
        # Tabela de transições
        self.tabela_transicoes = {
            EstadoAFD.Q0: {
                '_eh_letra_ou_underscore': EstadoAFD.Q1
            },
            EstadoAFD.Q1: {
                '_eh_alfanumerico_ou_underscore': EstadoAFD.Q1
            }
        }
    
    def _eh_letra_ou_underscore(self, char: str) -> bool:
        """Verifica se é letra (a-z, A-Z) ou underscore"""
        return char.isalpha() or char == '_'
    
    def _eh_alfanumerico_ou_underscore(self, char: str) -> bool:
        """Verifica se é letra, dígito ou underscore"""
        return char.isalnum() or char == '_'


class AFDNumeroInteiro(AFD):
    """
    AFD para reconhecer números inteiros
    
    PADRÃO: [0-9]+
    
    Estados:
    - q0: inicial
    - q1: final (viu pelo menos um dígito)
    
    Transições:
    - q0 --[0-9]--> q1
    - q1 --[0-9]--> q1
    """
    
    def __init__(self):
        super().__init__(estados_finais={EstadoAFD.Q1})
        
        self.tabela_transicoes = {
            EstadoAFD.Q0: {
                '_eh_digito': EstadoAFD.Q1
            },
            EstadoAFD.Q1: {
                '_eh_digito': EstadoAFD.Q1
            }
        }
    
    def _eh_digito(self, char: str) -> bool:
        """Verifica se é dígito (0-9)"""
        return char.isdigit()


class AFDNumeroReal(AFD):
    """
    AFD para reconhecer números reais
    
    PADRÃO: [0-9]+\.[0-9]+
    
    Estados:
    - q0: inicial
    - q1: viu dígitos antes do ponto
    - q2: final (viu dígitos após o ponto)
    
    Transições:
    - q0 --[0-9]--> q1
    - q1 --[0-9]--> q1
    - q1 --[.]--> q2
    - q2 --[0-9]--> q2
    """
    
    def __init__(self):
        super().__init__(estados_finais={EstadoAFD.Q2})
        
        self.tabela_transicoes = {
            EstadoAFD.Q0: {
                '_eh_digito': EstadoAFD.Q1
            },
            EstadoAFD.Q1: {
                '_eh_digito': EstadoAFD.Q1,
                '.': EstadoAFD.Q2
            },
            EstadoAFD.Q2: {
                '_eh_digito': EstadoAFD.Q2
            }
        }
    
    def _eh_digito(self, char: str) -> bool:
        """Verifica se é dígito (0-9)"""
        return char.isdigit()


class ValidadorTokensAFD:
    """
    Classe utilitária que usa AFDs para validar tokens
    
    Demonstra o uso prático dos AFDs na análise léxica.
    """
    
    def __init__(self):
        self.afd_identificador = AFDIdentificador()
        self.afd_numero_inteiro = AFDNumeroInteiro()
        self.afd_numero_real = AFDNumeroReal()
    
    def eh_identificador_valido(self, texto: str) -> bool:
        """
        Valida se o texto é um identificador válido
        
        Args:
            texto: String a validar
            
        Returns:
            bool: True se é identificador válido
            
        Exemplo:
            >>> validador = ValidadorTokensAFD()
            >>> validador.eh_identificador_valido("soma")
            True
            >>> validador.eh_identificador_valido("123abc")
            False
        """
        return self.afd_identificador.processar_string(texto)
    
    def eh_numero_inteiro_valido(self, texto: str) -> bool:
        """
        Valida se o texto é um número inteiro válido
        
        Args:
            texto: String a validar
            
        Returns:
            bool: True se é número inteiro válido
            
        Exemplo:
            >>> validador = ValidadorTokensAFD()
            >>> validador.eh_numero_inteiro_valido("123")
            True
            >>> validador.eh_numero_inteiro_valido("12.5")
            False
        """
        return self.afd_numero_inteiro.processar_string(texto)
    
    def eh_numero_real_valido(self, texto: str) -> bool:
        """
        Valida se o texto é um número real válido
        
        Args:
            texto: String a validar
            
        Returns:
            bool: True se é número real válido
            
        Exemplo:
            >>> validador = ValidadorTokensAFD()
            >>> validador.eh_numero_real_valido("3.14")
            True
            >>> validador.eh_numero_real_valido("123")
            False
        """
        return self.afd_numero_real.processar_string(texto)
    
    def identificar_tipo_token(self, texto: str) -> str:
        """
        Identifica o tipo de token usando AFDs
        
        Args:
            texto: String a identificar
            
        Returns:
            str: Tipo do token ('identificador', 'inteiro', 'real', 'desconhecido')
        """
        if self.eh_identificador_valido(texto):
            return 'identificador'
        elif self.eh_numero_real_valido(texto):
            return 'real'
        elif self.eh_numero_inteiro_valido(texto):
            return 'inteiro'
        else:
            return 'desconhecido'


def demonstrar_afd():
    """
    Função de demonstração dos AFDs
    
    Mostra o funcionamento prático dos autômatos finitos.
    """
    print("=" * 60)
    print("DEMONSTRAÇÃO DE AUTÔMATOS FINITOS DETERMINÍSTICOS (AFD)")
    print("=" * 60)
    
    validador = ValidadorTokensAFD()
    
    testes = [
        "soma",
        "_variavel",
        "var123",
        "123abc",
        "42",
        "3.14",
        "123.456.789",
        "abc_def_123"
    ]
    
    print("\nTESTES DE RECONHECIMENTO:")
    print("-" * 60)
    
    for teste in testes:
        tipo = validador.identificar_tipo_token(teste)
        print(f"'{teste:15}' → {tipo}")
    
    print("\n" + "=" * 60)
    print("EXPLICAÇÃO:")
    print("-" * 60)
    print("Cada teste acima passa por AFDs que simulam máquinas de estados")
    print("para reconhecer padrões específicos (identificadores, números).")
    print("\nAFDs garantem reconhecimento determinístico e eficiente!")
    print("=" * 60)


if __name__ == '__main__':
    # Executar demonstração
    demonstrar_afd()
