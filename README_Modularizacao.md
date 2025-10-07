# Compilador Portugol - Versão Modularizada

Este projeto implementa um compilador completo para a linguagem Portugol, seguindo as melhores práticas de engenharia de software com código modularizado e bem estruturado.

## 📁 Estrutura do Projeto

```
A3_Compiladores/
├── src/                    # Código fonte modularizado
│   ├── __init__.py         # Configuração do pacote
│   ├── exceptions.py       # Hierarquia de exceções
│   ├── ast_nodes.py        # Definições da AST
│   ├── lexer.py           # Analisador léxico
│   ├── parser.py          # Analisador sintático
│   ├── semantic.py        # Analisador semântico
│   ├── codegen.py         # Gerador de código
│   └── main.py            # Compilador principal
├── programa.py            # Versão monolítica original
├── programa.por           # Programa de teste
└── teste_modularizacao.py # Script de teste da modularização
```

## 🏗️ Arquitetura Modular

### 1. **src/exceptions.py** - Hierarquia de Exceções
- `CompiladorError`: Classe base para todos os erros
- `ErroLexico`: Erros na análise léxica
- `ErroSintatico`: Erros na análise sintática
- `ErroSemantico`: Erros na análise semântica

### 2. **src/ast_nodes.py** - Árvore Sintática Abstrata
- Definições de todos os nós da AST
- Classes para comandos, expressões e declarações
- Enumeração completa de tipos de tokens

### 3. **src/lexer.py** - Análise Léxica
- Tokenização do código fonte
- Reconhecimento de palavras-chave, operadores e literais
- Tratamento de comentários e espaços em branco

### 4. **src/parser.py** - Análise Sintática
- Implementação de descida recursiva
- Construção da AST a partir dos tokens
- Verificação da estrutura sintática

### 5. **src/semantic.py** - Análise Semântica
- Tabela de símbolos para variáveis
- Verificação de tipos e compatibilidade
- Validação de declarações e usos

### 6. **src/codegen.py** - Geração de Código
- Conversão da AST para código Python
- Mapeamento de construções Portugol → Python
- Formatação adequada do código gerado

### 7. **src/main.py** - Orquestração
- Coordenação de todas as fases de compilação
- Interface de linha de comando
- Modo debug e relatórios de erro

## 🚀 Como Usar

### Compilação de Arquivo
```python
from src import CompiladorPortugol

# Criar compilador
compilador = CompiladorPortugol(debug=True)

# Compilar arquivo
sucesso = compilador.compilar_arquivo("programa.por", "programa.py")
```

### Compilação de Código Diretamente
```python
codigo_portugol = """
inteiro x, y;
inicio
    x <- 10
    y <- x * 2
    escreva("Resultado:", y)
fim
"""

compilador = CompiladorPortugol()
codigo_python = compilador.compilar_codigo(codigo_portugol)
print(codigo_python)
```

### Via Linha de Comando
```bash
# Compilação normal
python -m src.main programa.por

# Com debug habilitado
python -m src.main programa.por --debug

# Visualizar tokens
python -m src.main programa.por --tokens
```

## 🧪 Execução dos Testes

Execute o teste de modularização:
```bash
python teste_modularizacao.py
```

Este teste executa um programa complexo com:
- Múltiplos tipos de variáveis
- Operações aritméticas e lógicas
- Estruturas condicionais aninhadas
- Entrada e saída de dados

## 🔧 Funcionalidades Suportadas

### Tipos de Dados
- `inteiro`: Números inteiros
- `real`: Números reais (ponto flutuante)
- `caracter`: Strings/texto
- `logico`: Valores booleanos (verdadeiro/falso)

### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`
- **Relacionais**: `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Lógicos**: `e` (and), `ou` (or)
- **Atribuição**: `<-`

### Estruturas de Controle
- **Condicional**: `se...entao...senao...fimse`
- **Repetição**: `enquanto...faca...fimenquanto`

### Entrada/Saída
- **Entrada**: `leia(variavel)`
- **Saída**: `escreva(expressao1, expressao2, ...)`

## 🎯 Vantagens da Modularização

### ✅ **Manutenibilidade**
- Cada módulo tem responsabilidade única
- Fácil localização e correção de bugs
- Modificações isoladas não afetam outros componentes

### ✅ **Testabilidade**
- Módulos podem ser testados independentemente
- Testes unitários específicos para cada fase
- Debugging mais eficiente

### ✅ **Reutilização**
- Componentes podem ser usados em outros projetos
- Implementação de diferentes backends (C++, Java, etc.)
- Extensibilidade para novas funcionalidades

### ✅ **Legibilidade**
- Código mais limpo e organizado
- Documentação clara de cada módulo
- Separação clara de responsabilidades

### ✅ **Escalabilidade**
- Fácil adição de novas funcionalidades
- Possibilidade de otimizações específicas
- Colaboração em equipe mais eficiente

## 📊 Comparação: Monolítico vs Modular

| Aspecto | Versão Monolítica | Versão Modular |
|---------|-------------------|----------------|
| **Linhas de código** | 771 linhas (1 arquivo) | ~800 linhas (7 arquivos) |
| **Responsabilidades** | Todas em uma classe | Separadas por módulo |
| **Testabilidade** | Difícil de testar partes | Testes unitários isolados |
| **Manutenção** | Alterações afetam tudo | Mudanças localizadas |
| **Colaboração** | Conflitos frequentes | Trabalho paralelo |
| **Debugging** | Stack traces complexos | Erros específicos por fase |

## 🔄 Processo de Compilação

```
Código Portugol
      ↓
[1] Lexer → Tokens
      ↓
[2] Parser → AST
      ↓
[3] Semantic → AST Validada
      ↓
[4] CodeGen → Código Python
```

Cada fase é implementada em um módulo separado, permitindo:
- **Debugging específico** de cada etapa
- **Otimizações independentes**
- **Extensões futuras** (novos backends, otimizações)

## 🏆 Conclusão

A modularização transformou um código monolítico de 771 linhas em uma arquitetura bem estruturada seguindo os princípios SOLID:

- **S**ingle Responsibility: Cada módulo tem uma responsabilidade
- **O**pen/Closed: Extensível sem modificar código existente
- **L**iskov Substitution: Componentes podem ser substituídos
- **I**nterface Segregation: Interfaces específicas e focadas
- **D**ependency Inversion: Dependências bem definidas

Esta estrutura serve como base sólida para futuras expansões e melhorias do compilador.