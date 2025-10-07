"""
Compilador Portugol - Interface de Linha de Comando

Uso:
    pytho                      if sucesso:
                if debug:
                    print("✅ Execução finalizada")
            else:
                print("❌ Falha na compilação")
                return 1
            
    except FileNotFoundError:
        print(f"❌ Arquivo '{arquivo_entrada}' não encontrado")
        return 1
    except Exception as e:
        print(f"❌ Erro: {e}")
        return 1           print("Erro: falha na compilação")
                return 1
            
    except FileNotFoundError:
        print(f"Erro: arquivo '{arquivo_entrada}' não encontrado")
        print("Certifique-se de que o arquivo existe no diretório atual")
        return 1
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())rquivo.por] [opções]
    
Opções:
    --debug         Exibe informações detalhadas de compilação
    --save          Salva o código Python gerado em arquivo
    
Exemplos:
    python compilar.py programa.por
    python compilar.py programa.por --debug
    python compilar.py programa.por --save
"""

import sys
from src import CompiladorPortugol

def main():
    # Configurações padrão
    arquivo_entrada = "programa.por"
    debug = False
    salvar = False
    
    # Processar argumentos
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == "--debug":
                debug = True
            elif arg == "--save":
                salvar = True
            elif arg.endswith(".por"):
                arquivo_entrada = arg
    
    print(f"🔧 Compilador Portugol")
    print(f"📁 Arquivo: {arquivo_entrada}")
    if debug:
        print(f"🐛 Debug: habilitado")
    if salvar:
        print(f"💾 Salvando arquivo Python")
    print("-" * 50)
    
    # Executar compilador
    compilador = CompiladorPortugol(debug=debug)
    
    try:
        if salvar:
            # Salvar arquivo e executar
            sucesso = compilador.compilar_arquivo(arquivo_entrada, salvar_arquivo=True)
            
            if sucesso:
                arquivo_saida = arquivo_entrada.replace('.por', '.py')
                print(f"✅ Arquivo gerado: {arquivo_saida}")
                
                resposta = input("🚀 Executar código? (s/n): ").lower()
                if resposta in ['s', 'sim', 'y', 'yes']:
                    print("Executando...")
                    print("-" * 30)
                    
                    with open(arquivo_saida, 'r', encoding='utf-8') as f:
                        codigo_gerado = f.read()
                    
                    exec(codigo_gerado)
                    print("-" * 30)
                    print("✅ Execução finalizada")
        else:
            # Execução direta
            sucesso = compilador.compilar_arquivo(arquivo_entrada, salvar_arquivo=False)
            
            if sucesso:
                if debug:
                    print("Compilação e execução finalizadas")
            else:
                print("Erro: falha na compilação")
                return 1
            
    except FileNotFoundError:
        print(f"❌ Arquivo '{arquivo_entrada}' não encontrado!")
        print("💡 Certifique-se de que o arquivo existe no diretório atual")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())