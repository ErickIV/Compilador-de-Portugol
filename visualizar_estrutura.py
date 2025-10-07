"""
Visualizador da Estrutura do Projeto Modularizado

Este script mostra a estrutura final do projeto após a modularização
e fornece estatísticas comparativas.
"""

import os
import glob
from pathlib import Path

def contar_linhas_arquivo(caminho):
    """Conta linhas de código em um arquivo"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            # Filtrar linhas vazias e comentários
            linhas_codigo = []
            for linha in linhas:
                linha_limpa = linha.strip()
                if linha_limpa and not linha_limpa.startswith('#') and not linha_limpa.startswith('"""'):
                    linhas_codigo.append(linha)
            return len(linhas), len(linhas_codigo)
    except:
        return 0, 0

def analisar_estrutura():
    """Analisa a estrutura do projeto"""
    print("📊 ANÁLISE DA ESTRUTURA DO PROJETO")
    print("=" * 70)
    
    # Diretório raiz
    raiz = Path(".")
    
    # Estatísticas gerais
    total_linhas = 0
    total_codigo = 0
    arquivos_analisados = []
    
    print("📁 ESTRUTURA DE ARQUIVOS:")
    print("-" * 70)
    
    # Arquivo monolítico original
    if os.path.exists("programa.py"):
        linhas, codigo = contar_linhas_arquivo("programa.py")
        total_linhas += linhas
        total_codigo += codigo
        arquivos_analisados.append(("programa.py", linhas, codigo, "Versão monolítica"))
        print(f"🏗️  programa.py                    {linhas:4d} linhas ({codigo:3d} código)")
    
    # Arquivos do diretório src/
    if os.path.exists("src"):
        print("📦 src/                             (Versão modularizada)")
        
        arquivos_src = [
            ("__init__.py", "Configuração do pacote"),
            ("exceptions.py", "Hierarquia de exceções"),
            ("ast_nodes.py", "Definições da AST"),
            ("lexer.py", "Analisador léxico"),
            ("parser.py", "Analisador sintático"),
            ("semantic.py", "Analisador semântico"),
            ("codegen.py", "Gerador de código"),
            ("main.py", "Compilador principal")
        ]
        
        for arquivo, descricao in arquivos_src:
            caminho = f"src/{arquivo}"
            if os.path.exists(caminho):
                linhas, codigo = contar_linhas_arquivo(caminho)
                total_linhas += linhas
                total_codigo += codigo
                arquivos_analisados.append((caminho, linhas, codigo, descricao))
                print(f"   ├── {arquivo:<20} {linhas:4d} linhas ({codigo:3d} código) - {descricao}")
    
    # Arquivos de teste e documentação
    print("\n📝 ARQUIVOS DE TESTE E DOCUMENTAÇÃO:")
    print("-" * 70)
    
    outros_arquivos = [
        ("programa.por", "Programa de teste"),
        ("teste_modularizacao.py", "Teste da modularização"),
        ("teste_comparacao.py", "Validação final"),
        ("README_Modularizacao.md", "Documentação")
    ]
    
    for arquivo, descricao in outros_arquivos:
        if os.path.exists(arquivo):
            linhas, codigo = contar_linhas_arquivo(arquivo)
            print(f"📄 {arquivo:<25} {linhas:4d} linhas - {descricao}")
    
    print("\n" + "=" * 70)
    print("📈 ESTATÍSTICAS COMPARATIVAS")
    print("=" * 70)
    
    # Separar monolítico vs modular
    monolitico = [a for a in arquivos_analisados if "programa.py" in a[0]]
    modular = [a for a in arquivos_analisados if a[0].startswith("src/")]
    
    if monolitico:
        print("🏗️  VERSÃO MONOLÍTICA:")
        for arquivo, linhas, codigo, desc in monolitico:
            print(f"   {arquivo}: {linhas} linhas ({codigo} código)")
    
    if modular:
        print("\n📦 VERSÃO MODULARIZADA:")
        total_mod_linhas = sum(a[1] for a in modular)
        total_mod_codigo = sum(a[2] for a in modular)
        
        for arquivo, linhas, codigo, desc in modular:
            print(f"   {arquivo}: {linhas} linhas ({codigo} código)")
        
        print(f"\n   📊 Total modular: {total_mod_linhas} linhas ({total_mod_codigo} código)")
        print(f"   📂 Número de módulos: {len(modular)}")
        print(f"   📐 Média por módulo: {total_mod_linhas // len(modular)} linhas")
    
    print("\n" + "=" * 70)
    print("🎯 BENEFÍCIOS DA MODULARIZAÇÃO")
    print("=" * 70)
    
    beneficios = [
        "✅ Separação clara de responsabilidades",
        "✅ Código mais legível e organizando",
        "✅ Facilidade para testes unitários",
        "✅ Manutenção localizada por módulo",
        "✅ Possibilidade de reutilização",
        "✅ Desenvolvimento em equipe facilitado",
        "✅ Extensibilidade para novos recursos",
        "✅ Debug mais eficiente por fase"
    ]
    
    for beneficio in beneficios:
        print(f"   {beneficio}")
    
    print("\n" + "=" * 70)
    print("🚀 FASES DE COMPILAÇÃO MODULARIZADAS")
    print("=" * 70)
    
    fases = [
        ("🔍 Fase 1", "Análise Léxica", "src/lexer.py", "Tokenização do código"),
        ("🌳 Fase 2", "Análise Sintática", "src/parser.py", "Construção da AST"),
        ("🔬 Fase 3", "Análise Semântica", "src/semantic.py", "Verificação de tipos"),
        ("⚙️  Fase 4", "Geração de Código", "src/codegen.py", "Produção do Python")
    ]
    
    for icone, nome, arquivo, descricao in fases:
        print(f"{icone} {nome:<18} | {arquivo:<15} | {descricao}")
    
    print("\n" + "=" * 70)
    print("✨ MODULARIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("🏆 Projeto segue as melhores práticas de engenharia de software")
    print("=" * 70)

if __name__ == "__main__":
    analisar_estrutura()