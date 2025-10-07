"""
Compilador Portugol - Interface de Linha de Comando

Uso:
    python compilar.py [arquivo.por] [opções]
    
Opções:
    --debug         Exibe informações detalhadas de compilação
    --save          Salva o código Python gerado em arquivo
    
Exemplos:
    python compilar.py programa.por
    python compilar.py programa.por --debug
    python compilar.py programa.por --save
"""

import sys
from src.main import CompiladorPortugol

def main():
    # Configurações padrão
    arquivo_entrada = "programa.por"
    debug = False
    salvar = False
    
    # Processar argumentos
    args = sys.argv[1:]
    
    # Primeiro argumento é o arquivo (se fornecido)
    if args and not args[0].startswith('--'):
        arquivo_entrada = args[0]
        args = args[1:]
    
    # Processar opções
    for arg in args:
        if arg == '--debug':
            debug = True
        elif arg == '--save':
            salvar = True
        elif arg == '--help' or arg == '-h':
            print(__doc__)
            return 0
        else:
            print(f"Opção desconhecida: {arg}")
            print("Use --help para ver as opções disponíveis")
            return 1
    
    # Exibir cabeçalho
    print("🔧 Compilador Portugol")
    print(f"📁 Arquivo: {arquivo_entrada}")
    print("-" * 50)
    
    try:
        # Criar compilador
        compilador = CompiladorPortugol(debug=debug)
        
        # Compilar e executar
        if debug:
            print("🔍 Modo debug ativado")
        
        sucesso = compilador.compilar_arquivo(arquivo_entrada, salvar_arquivo=salvar)
        
        if sucesso:
            if debug:
                print("✅ Execução finalizada")
        else:
            print("❌ Erro: falha na compilação")
            return 1
            
    except FileNotFoundError:
        print(f"❌ Erro: arquivo '{arquivo_entrada}' não encontrado")
        print("Certifique-se de que o arquivo existe no diretório atual")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())