"""
Compilador Portugol - Módulo Principal

Este módulo orquestra todo o processo de compilação:
1. Análise Léxica (Lexer)
2. Análise Sintática (Parser) 
3. Análise Semântica (Semantic)
4. Geração de Código (CodeGen)
"""

import sys
from typing import Optional
from .lexer import Lexer
from .parser import Parser
from .semantic import AnalisadorSemantico
from .codegen import GeradorDeCodigo
from .exceptions import CompiladorError


class CompiladorPortugol:
    """
    Compilador principal para a linguagem Portugol
    
    Coordena todas as fases da compilação e fornece interface
    unificada para o processo de compilação completo.
    """
    
    def __init__(self, debug: bool = False):
        """
        Inicializa o compilador
        
        Args:
            debug: Se True, imprime informações de debug
        """
        self.debug = debug

    def compilar_arquivo(self, caminho_arquivo: str, 
                        arquivo_saida: Optional[str] = None,
                        salvar_arquivo: bool = False) -> bool:
        """
        Compila um arquivo Portugol para Python
        
        Args:
            caminho_arquivo: Caminho para o arquivo .por
            arquivo_saida: Caminho para o arquivo Python de saída (opcional)
            salvar_arquivo: Se True, salva o arquivo Python gerado
            
        Returns:
            bool: True se compilação foi bem-sucedida, False caso contrário
        """
        try:
            # Ler arquivo fonte
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                codigo_fonte = arquivo.read()
            
            # Compilar código
            codigo_python = self.compilar_codigo(codigo_fonte)
            
            if codigo_python is None:
                return False
            
            # Salvar arquivo apenas se solicitado
            if salvar_arquivo:
                if arquivo_saida is None:
                    arquivo_saida = caminho_arquivo.replace('.por', '.py')
                
                with open(arquivo_saida, 'w', encoding='utf-8') as arquivo:
                    arquivo.write(codigo_python)
                
                if self.debug:
                    print(f"✓ Arquivo salvo: {arquivo_saida}")
            
            # Executar código diretamente
            if self.debug:
                print("🚀 Executando...")
                print("-" * 30)
            
            # Criar namespace global para execução
            global_namespace = {
                '__name__': '__main__',
                '__builtins__': __builtins__
            }
            
            # Executar código Python
            exec(codigo_python, global_namespace)
            
            if self.debug:
                print("-" * 30)
                print("✅ Execução concluída")
            
            return True
            
        except FileNotFoundError:
            print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False

    def compilar_codigo(self, codigo_fonte: str) -> Optional[str]:
        """
        Compila código Portugol para Python
        
        Args:
            codigo_fonte: Código fonte em Portugol
            
        Returns:
            str: Código Python gerado, ou None se houve erro
        """
        try:
            if self.debug:
                print("📝 Iniciando compilação...")
                print("=" * 40)
            
            # Fase 1: Análise Léxica
            if self.debug:
                print("🔍 Análise Léxica")
            
            lexer = Lexer(codigo_fonte)
            
            if self.debug:
                print("   ✓ Lexer inicializado")
            
            # Fase 2: Análise Sintática
            if self.debug:
                print("🌳 Análise Sintática")
            
            parser = Parser(lexer)
            ast = parser.analisar()
            
            if self.debug:
                print("   ✓ AST construída")
                print(f"   - Declarações: {len(ast.declaracoes)}")
                print(f"   - Comandos: {len(ast.comandos)}")
            
            # Fase 3: Análise Semântica
            if self.debug:
                print("🔬 Análise Semântica")
            
            analisador_semantico = AnalisadorSemantico()
            analisador_semantico.analisar(ast)
            
            if self.debug:
                print("   ✓ Análise concluída")
                print(f"   - Variáveis: {len(analisador_semantico.tabela_simbolos.simbolos)}")
            
            # Fase 4: Geração de Código
            if self.debug:
                print("⚙️  Geração de Código")
            
            gerador = GeradorDeCodigo()
            codigo_python = gerador.gerar(ast)
            
            if self.debug:
                print("   ✓ Código gerado")
                print(f"   - Linhas: {len(codigo_python.split())}")
                print("=" * 40)
                print("✅ Compilação concluída")
            
            return codigo_python
            
        except CompiladorError as e:
            print(f"❌ Erro de compilação: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado durante compilação: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return None

    def executar_compilacao_e_teste(self, codigo_fonte: str) -> bool:
        """
        Compila e executa o código para teste
        
        Args:
            codigo_fonte: Código fonte em Portugol
            
        Returns:
            bool: True se compilação e execução foram bem-sucedidas
        """
        try:
            # Compilar
            codigo_python = self.compilar_codigo(codigo_fonte)
            
            if codigo_python is None:
                return False
            
            if self.debug:
                print("\n🚀 Executando código gerado:")
                print("-" * 30)
            
            # Executar código Python gerado
            exec(codigo_python)
            
            if self.debug:
                print("-" * 30)
                print("✅ Execução concluída com sucesso!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            if self.debug:
                import traceback
                traceback.print_exc()
            return False

    def listar_tokens(self, codigo_fonte: str) -> None:
        """
        Lista todos os tokens do código fonte (para debug)
        
        Args:
            codigo_fonte: Código fonte em Portugol
        """
        try:
            print("🔍 Análise de Tokens:")
            print("-" * 40)
            
            lexer = Lexer(codigo_fonte)
            tokens = []
            
            while True:
                token = lexer.proximo_token()
                tokens.append(token)
                
                print(f"  {token.tipo.value:15} | {token.lexema:10} | L:{token.linha} C:{token.coluna}")
                
                if token.tipo.value == 'EOF':
                    break
            
            print("-" * 40)
            print(f"Total de tokens: {len(tokens)}")
            
        except CompiladorError as e:
            print(f"❌ Erro na análise léxica: {e}")


def main():
    """Função principal para uso via linha de comando"""
    if len(sys.argv) < 2:
        print("Uso: python -m src.main <arquivo.por> [--debug] [--save]")
        print("Exemplo: python -m src.main programa.por --debug")
        print("         python -m src.main programa.por --save  # Para salvar arquivo .py")
        return
    
    arquivo_entrada = sys.argv[1]
    debug = '--debug' in sys.argv
    salvar = '--save' in sys.argv
    
    compilador = CompiladorPortugol(debug=debug)
    
    if '--tokens' in sys.argv:
        # Modo de listagem de tokens
        try:
            with open(arquivo_entrada, 'r', encoding='utf-8') as f:
                codigo = f.read()
            compilador.listar_tokens(codigo)
        except FileNotFoundError:
            print(f"Arquivo '{arquivo_entrada}' não encontrado.")
    else:
        # Compilação normal
        sucesso = compilador.compilar_arquivo(arquivo_entrada, salvar_arquivo=salvar)
        sys.exit(0 if sucesso else 1)


if __name__ == '__main__':
    main()