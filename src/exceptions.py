"""
Exceções customizadas do compilador Portugol

Este módulo define uma hierarquia de exceções específicas para diferentes
fases da compilação, facilitando o tratamento de erros e debugging.
"""

from typing import Optional


class CompiladorError(Exception):
    """Classe base para todos os erros do compilador"""
    
    def __init__(self, mensagem: str, linha: int = 0, coluna: int = 0):
        self.mensagem = mensagem
        self.linha = linha
        self.coluna = coluna
        super().__init__(self._formatar_mensagem())
    
    def _formatar_mensagem(self) -> str:
        """Formata a mensagem de erro com informações de localização"""
        if self.linha > 0:
            return f"{self.mensagem} (linha {self.linha}, coluna {self.coluna})"
        return self.mensagem


class ErroLexico(CompiladorError):
    """Erro durante a análise léxica (tokenização)"""
    pass


class ErroSintatico(CompiladorError):
    """Erro durante a análise sintática (parsing)"""
    pass


class ErroSemantico(CompiladorError):
    """Erro durante a análise semântica (validação de tipos)"""
    pass


class ErroGeracaoCodigo(CompiladorError):
    """Erro durante a geração de código"""
    pass