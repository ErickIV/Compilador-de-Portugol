<div align="center">

# 🔧 Compilador Portugol

### _Tradutor educacional de Portugol para Python_

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-98%20passing-success.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-80%25-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Arquitetura](https://img.shields.io/badge/Arquitetura-Modular-orange.svg)]()

</div>

---

## 📋 Sobre o Projeto

Este projeto implementa um **compilador completo** para a linguagem **Portugol** (.por), traduzindo código educacional em português para Python executável. Desenvolvido com arquitetura modular seguindo as **6 fases clássicas de compilação**, incluindo geração de código intermediário e otimizações.

**🎓 Contexto Acadêmico:** Projeto desenvolvido para a UC de Teoria da Computação e Compiladores - UNISUL

### ✨ **Novidades - Versão 2.1**

🚀 **Fases Completas de Compilação:**

- ✅ Análise Léxica com Expressões Regulares documentadas
- ✅ Autômatos Finitos Determinísticos (AFD) explícitos
- ✅ Geração de Código Intermediário (3 endereços)
- ✅ 5 tipos de Otimizações implementadas
- ✅ Comparação de código antes/depois das otimizações

🔥 **Correções e Melhorias Críticas:**

- ✅ **BUG CRÍTICO CORRIGIDO:** Loops com passo negativo agora funcionam corretamente
- ✅ **NOVA FEATURE:** Cláusula `passo` opcional no loop `para` (padrão = 1)
- ✅ Tratamento completo de caracteres de escape em strings (`\"`, `\\`, `\n`)
- ✅ Documentação corrigida e atualizada

🧪 **Suite de Testes Profissional:**

- ✅ **98 testes automatizados** cobrindo todas as fases
- ✅ **~80% de cobertura** de código
- ✅ Testes unitários, de integração e end-to-end
- ✅ Fixtures reutilizáveis para cenários comuns

---

## 📁 Estrutura do Projeto

```
Compilador-de-Portugol/
├── 📂 src/                      # Código fonte modularizado
│   ├── __init__.py              # Configuração do pacote
│   ├── exceptions.py            # Hierarquia de exceções personalizadas
│   ├── ast_nodes.py             # Definições da AST (Árvore Sintática Abstrata)
│   ├── lexer.py                 # 🔤 Analisador Léxico (Tokenização + ERs)
│   ├── automaton.py             # 🤖 Autômatos Finitos Determinísticos (AFD)
│   ├── parser.py                # 📝 Analisador Sintático (Construção da AST)
│   ├── semantic.py              # ✅ Analisador Semântico (Validação)
│   ├── intermediate.py          # 🔄 Gerador de Código Intermediário (3 endereços)
│   ├── optimizer.py             # ⚡ Otimizador de Código
│   ├── codegen.py               # 🐍 Gerador de Código Python
│   └── main.py                  # 🎯 Orquestrador principal
│
├── 📂 tests/                    # Suite de testes [NOVO]
│   ├── conftest.py              # 🔧 Configuração e fixtures
│   ├── test_lexer.py            # 🔤 Testes da análise léxica
│   ├── test_parser.py           # 📝 Testes da análise sintática (35 testes)
│   ├── test_semantic.py         # ✅ Testes da análise semântica (26 testes)
│   ├── test_codegen.py          # 🐍 Testes de geração de código (23 testes)
│   └── test_integration.py      # 🔗 Testes end-to-end (14 testes)
│
├── 📂 exemplos/                 # Programas de demonstração
│   ├── demo_completa.por        # 🚀 Demonstração completa (não-interativo)
│   ├── calculadora_imc.por      # 💊 Calculadora de IMC (interativo)
│   ├── bubble_sort.por          # 🔢 Algoritmo de ordenação
│   ├── teste_otimizacoes.por    # ⚡ Teste de otimizações
│   ├── fibonacci.por            # 🔁 Sequência de Fibonacci (loop 'para')
│   ├── fatorial.por             # 🧮 Fatorial e potenciação (^)
│   ├── teste_modulo.por         # ➗ Operador módulo (%) e paridade
│   ├── teste_loop_reverso.por   # 🔄 Loop com passo negativo [NOVO]
│   └── teste_string_escape.por  # 📝 Tratamento de escape [NOVO]
│
├── compilar.py                  # 🖥️  Interface CLI
├── programa.por                 # 📄 Programa exemplo
└── README.md                    # 📖 Documentação
```

---

## 🏗️ Arquitetura Modular

### 🔤 **1. Análise Léxica** (`lexer.py` + `automaton.py`)

Transforma o código fonte em **tokens** (unidades léxicas).

**Funcionalidades:**

- ✅ Reconhece palavras-chave (`inicio`, `fim`, `se`, `enquanto`, `para`, etc.)
- ✅ Identifica operadores aritméticos (`+`, `-`, `*`, `/`, `%`, `^`)
- ✅ Identifica operadores relacionais (`==`, `!=`, `<`, `<=`, `>`, `>=`)
- ✅ Identifica operadores lógicos (`e`, `ou`, `nao`)
- ✅ Processa literais (números, strings, booleanos)
- ✅ Ignora comentários (`//` e `/* */`)
- ✅ Rastreia posição (linha e coluna) para mensagens de erro
- ✅ Trata caracteres de escape em strings (`\"`, `\\`, `\n`, `\t`)
- ✨ **NOVO:** Expressões Regulares formalmente documentadas
- ✨ **NOVO:** AFDs explícitos para reconhecimento educacional

**Exemplo de Token:**

```python
Token(tipo=TipoToken.INTEIRO, lexema="42", linha=5, coluna=12)
```

---

### 📝 **2. Análise Sintática** (`parser.py`)

Constrói a **Árvore Sintática Abstrata (AST)** a partir dos tokens.

**Funcionalidades:**

- ✅ Parser de descida recursiva
- ✅ Verifica estrutura gramatical do programa
- ✅ Valida declarações de variáveis
- ✅ Processa comandos e expressões
- ✅ Implementa precedência de operadores
- ✨ **NOVO:** Cláusula `passo` opcional no loop `para` (padrão = 1)

**Exemplo de Sintaxe (Loop Para):**

```portugol
// Antes (v2.0): passo obrigatório
para i de 1 ate 10 passo 1 faca
    escreva(i)
fimpara

// Agora (v2.1): passo opcional
para i de 1 ate 10 faca
    escreva(i)
fimpara

// Passo negativo (contagem regressiva)
para i de 10 ate 1 passo -1 faca
    escreva(i)
fimpara
```

---

### ✅ **3. Análise Semântica** (`semantic.py`)

Valida o **significado** do programa.

**Funcionalidades:**

- ✅ Verifica se variáveis foram declaradas antes do uso
- ✅ Valida compatibilidade de tipos em operações
- ✅ Detecta variáveis não inicializadas (warnings)
- ✅ Mantém tabela de símbolos (escopo de variáveis)
- ✅ Verifica coerência lógica

**Exemplo de Validação:**

```portugol
inteiro x;
inicio
    y <- 10  // ERRO: variável 'y' não declarada
fim
```

---

### 🔄 **4. Geração de Código Intermediário** (`intermediate.py`)

Gera representação de **3 endereços** para facilitar otimizações.

**Funcionalidades:**

- ✅ Linearização da AST em instruções sequenciais
- ✅ Cada instrução tem no máximo 3 operandos
- ✅ Suporta labels e saltos condicionais
- ✅ Base para aplicação de otimizações

**Exemplo:**

```
Portugol:                  Código Intermediário:
inteiro a, b, c;          a = 5
inicio                     b = 10
    a <- 5                 t1 = a + b
    b <- 10                c = t1
    c <- a + b
fim
```

---

### ⚡ **5. Otimização** (`optimizer.py`)

Aplica transformações que preservam semântica mas melhoram desempenho.

**Técnicas Implementadas:**

| Otimização                      | Descrição                                  | Exemplo                            |
| ------------------------------- | ------------------------------------------ | ---------------------------------- |
| 🔢 **Constant Folding**         | Avalia constantes em tempo de compilação   | `x <- 2 + 3` → `x <- 5`            |
| 🔄 **Constant Propagation**     | Substitui variáveis por valores conhecidos | `x <- 5; y <- x` → `y <- 5`        |
| ➕ **Algebraic Simplification** | Aplica identidades matemáticas             | `x <- y + 0` → `x <- y`            |
| 📋 **Copy Propagation**         | Elimina cópias desnecessárias              | `a <- b; c <- a` → `c <- b`        |
| 🗑️ **Dead Code Elimination**    | Remove código não utilizado                | Remove variáveis não referenciadas |

**Redução de Código:** Até **29.7%** com otimizações ativas!

---

### 🐍 **6. Geração de Código Final** (`codegen.py`)

Traduz a AST para **código Python** executável.

**Funcionalidades:**

- ✅ Converte tipos Portugol → Python (`inteiro` → `int`, `caracter` → `str`)
- ✅ Traduz estruturas de controle (`se-entao` → `if-else`, `enquanto` → `while`)
- ✅ Implementa entrada/saída (`leia()` → `input()`, `escreva()` → `print()`)
- ✅ Gera código formatado e legível
- ✅ Preserva semântica original
- ✨ **BUG CRÍTICO CORRIGIDO:** Condição dinâmica para loops com passo negativo

**Exemplo de Tradução (Loop Reverso):**

```portugol
// Portugol
inteiro i;
inicio
    para i de 10 ate 1 passo -1 faca
        escreva(i)
    fimpara
fim
```

```python
# Python gerado (v2.1 - CORRIGIDO)
def main():
    i = 0
    i = 10
    while ((-1) > 0 and i <= 1) or ((-1) < 0 and i >= 1):
        print(i)
        i = i + (-1)

if __name__ == '__main__':
    main()
```

**Antes (v2.0):** Loop com passo negativo não executava (condição sempre falsa)
**Agora (v2.1):** Condição dinâmica detecta sinal do passo em runtime ✅

---

## 📥 Instalação

```bash
# Clone o repositório
git clone https://github.com/ErickIV/Compilador-de-Portugol.git
cd Compilador-de-Portugol

# Verificar versão do Python (requer 3.11+)
python --version

# Instalar pytest para rodar os testes (opcional)
pip install pytest
```

**Pronto!** O compilador usa apenas a biblioteca padrão do Python, não requer outras dependências.

---

## 🚀 Como Usar

### 💻 **Método 1: Interface CLI (Recomendado)**

```bash
# Compilar e executar diretamente
python compilar.py programa.por

# Modo debug (mostra todas as fases)
python compilar.py programa.por --debug

# Salvar código Python gerado
python compilar.py programa.por --save

# Mostrar código intermediário (3 endereços)
python compilar.py programa.por --intermediate

# Aplicar otimizações + mostrar antes/depois
python compilar.py programa.por --intermediate --optimize

# Demonstrar AFDs de reconhecimento de tokens
python compilar.py programa.por --show-afd

# Modo completo (todas as fases)
python compilar.py programa.por --debug --intermediate --optimize
```

### 📊 **Flags Disponíveis**

| Flag             | Descrição                                                                                                                                                                                                                 | Exemplo                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `--intermediate` | Mostra código intermediário de 3 endereços                                                                                                                                                                                | `python compilar.py teste.por --intermediate`            |
| `--optimize`     | Aplica otimizações (requer `--intermediate`)                                                                                                                                                                              | `python compilar.py teste.por --intermediate --optimize` |
| `--show-afd`     | Demonstra AFDs para tokens (educacional)                                                                                                                                                                                  | `python compilar.py teste.por --show-afd`                |
| `--debug`        | Mostra todas as fases detalhadamente                                                                                                                                                                                      | `python compilar.py teste.por --debug`                   |
| `--save`         | Salva arquivo .py gerado                                                                                                                                                                                                  | `python compilar.py teste.por --save`                    |
| `--debugpro`     | Modo de debug passo-a-passo (muito verboso): mostra processamento caractere-a-caractere no lexer, tokens reconhecidos, avanço do parser, passos da análise semântica, instruções adicionadas ao IR e passos do otimizador | `python compilar.py teste.por --debugpro`                |

---

**Sobre `--debugpro`:**

- `--debugpro` é um modo de depuração extremamente verboso pensado para fins educacionais e diagnóstico. Quando ativado, o compilador imprime:

  - O lexer processando cada caractere e mensagens quando tokens são reconhecidos;
  - O parser mostrando avanços e consumo de tokens (token-a-token);
  - Mensagens da análise semântica para declarações e comandos analisados;
  - Cada instrução criada no código intermediário (IR) enquanto a IR é gerada;
  - Passos e relatórios do otimizador durante as passadas de transformação.

- Use `--debugpro` para entender internamente como cada fase funciona ou para depurar casos complexos. A saída pode ser muito extensa; combine com redirecionamento para arquivo quando necessário:

```powershell
python compilar.py exemplos/demo_completa.por --debugpro > debug_pro_output.txt
```

-- Para inspeção menos verbosa, prefira `--debug` (mostra resumo das fases) ou `--intermediate` (mostra IR).

### 🐍 **Método 2: Como Módulo Python**

```python
from src.main import CompiladorPortugol

# Criar compilador
compilador = CompiladorPortugol(debug=True)

# Compilar e executar arquivo
sucesso = compilador.compilar_arquivo("programa.por")

# Compilar código direto
codigo_portugol = """
inteiro x;
inicio
    x <- 42
    escreva("Valor:", x)
fim
"""
sucesso = compilador.executar_compilacao_e_teste(codigo_portugol)
```

---

### 🧪 **Método 3: Executar Testes**

```bash
# Executar todos os 98 testes
python -m pytest tests/ -v

# Executar testes específicos
python -m pytest tests/test_parser.py -v
python -m pytest tests/test_codegen.py -v
python -m pytest tests/test_integration.py -v

# Executar com cobertura de código
python -m pytest tests/ --cov=src --cov-report=html
```

**Suite de Testes:**

- ✅ `test_lexer.py` - Testes do analisador léxico
- ✅ `test_parser.py` - 35 testes do parser (incluindo passo opcional)
- ✅ `test_semantic.py` - 26 testes de análise semântica
- ✅ `test_codegen.py` - 23 testes de geração de código (incluindo loops reversos)
- ✅ `test_integration.py` - 14 testes end-to-end

---

## 📚 Especificação da Linguagem Portugol

### 🔤 **Tipos de Dados**

| Tipo       | Descrição        | Exemplo               | Python Equivalente |
| ---------- | ---------------- | --------------------- | ------------------ |
| `inteiro`  | Números inteiros | `42`, `-10`           | `int`              |
| `real`     | Números decimais | `3.14`, `-0.5`        | `float`            |
| `caracter` | Strings de texto | `"Olá mundo"`         | `str`              |
| `logico`   | Booleanos        | `verdadeiro`, `falso` | `bool`             |

### 🎯 **Operadores**

**Aritméticos:**

- `+` Adição
- `-` Subtração
- `*` Multiplicação
- `/` Divisão
- `%` Módulo (resto da divisão)
- `^` Potenciação

**Relacionais:**

- `==` Igual
- `!=` Diferente
- `<` Menor que
- `<=` Menor ou igual
- `>` Maior que
- `>=` Maior ou igual

**Lógicos:**

- `e` AND lógico
- `ou` OR lógico
- `nao` NOT lógico

### 📝 **Estruturas de Controle**

**Condicional:**

```portugol
se condicao entao
    // comandos
senao
    // comandos alternativos
fimse
```

**Loop Enquanto:**

```portugol
enquanto condicao faca
    // comandos
fimenquanto
```

**Loop Para (com passo opcional):**

```portugol
// Passo positivo (padrão = 1)
para i de 1 ate 10 faca
    escreva(i)
fimpara

// Passo explícito
para i de 0 ate 100 passo 10 faca
    escreva(i)
fimpara

// Passo negativo (contagem regressiva)
para i de 10 ate 1 passo -1 faca
    escreva(i)
fimpara
```

### 📥📤 **Entrada e Saída**

```portugol
// Entrada
leia(variavel)

// Saída
escreva("Texto", variavel, expressao)
```

### 💬 **Comentários**

```portugol
// Comentário de linha única

/*
   Comentário
   de múltiplas
   linhas
*/
```

---

## 🎯 Exemplos de Uso

### 📝 **Programa Básico**

```portugol
inteiro x, y, soma;

inicio
    escreva("Digite o primeiro número:")
    leia(x)

    escreva("Digite o segundo número:")
    leia(y)

    soma <- x + y

    escreva("A soma é:", soma)
fim
```

### 🔁 **Fibonacci com Loop Reverso**

```portugol
inteiro n, a, b, temp, i;

inicio
    escreva("Quantos termos da sequência?")
    leia(n)

    a <- 0
    b <- 1

    escreva("Sequência de Fibonacci:")
    escreva(a)
    escreva(b)

    // Loop com passo padrão (1)
    para i de 2 ate n faca
        temp <- a + b
        escreva(temp)
        a <- b
        b <- temp
    fimpara

    // Agora em ordem reversa
    escreva("Ordem reversa:")
    para i de n ate 1 passo -1 faca
        escreva("Posição:", i)
    fimpara
fim
```

### 📝 **Strings com Escape**

```portugol
caracter texto, caminho;

inicio
    // Aspas escapadas
    texto <- "Ele disse: \"Olá, mundo!\""
    escreva(texto)

    // Barras invertidas
    caminho <- "C:\\Users\\Documents\\arquivo.txt"
    escreva("Caminho:", caminho)

    // Newline
    texto <- "Linha 1\nLinha 2"
    escreva(texto)
fim
```

---

## 🔍 Exemplo de Execução Detalhada

### Arquivo: `teste.por`

```portugol
inteiro x, y;
inicio
    x <- 5 + 3
    y <- x * 2
    escreva("Resultado:", y)
fim
```

### 🖥️ Execução Completa:

```bash
python compilar.py teste.por --debug --intermediate --optimize
```

**Saída:**

```
=== FASE 1: ANÁLISE LÉXICA ===
Tokens encontrados: 23
- INTEIRO (linha 1, coluna 1)
- IDENTIFICADOR 'x' (linha 1, coluna 9)
- VIRGULA (linha 1, coluna 10)
...

=== FASE 2: ANÁLISE SINTÁTICA ===
AST construída com sucesso
- Programa com 2 declarações e 3 comandos

=== FASE 3: ANÁLISE SEMÂNTICA ===
Validação concluída com sucesso
Tabela de símbolos:
  - x: inteiro (inicializada)
  - y: inteiro (inicializada)

=== FASE 4: CÓDIGO INTERMEDIÁRIO ===
1: x = 5 + 3
2: t1 = x * 2
3: y = t1
4: print "Resultado:" y

=== FASE 5: OTIMIZAÇÕES ===
Aplicando Constant Folding...
Aplicando Constant Propagation...
Aplicando Algebraic Simplification...
Redução de código: 25.0%

Código otimizado:
1: x = 8
2: y = 16
3: print "Resultado:" y

=== FASE 6: GERAÇÃO DE CÓDIGO PYTHON ===
def main():
    x = 8
    y = 16
    print("Resultado:", y)

if __name__ == '__main__':
    main()

=== EXECUÇÃO ===
Resultado: 16

✅ Compilação e execução bem-sucedidas!
```

---

## 🧪 Testes Automatizados

O projeto inclui uma suite completa de **98 testes** organizados por fase:

### 📊 **Estatísticas de Testes**

| Arquivo               | Testes | Descrição                         |
| --------------------- | ------ | --------------------------------- |
| `test_lexer.py`       | 3      | Tokenização e escape de strings   |
| `test_parser.py`      | 35     | Construção da AST, passo opcional |
| `test_semantic.py`    | 26     | Validação semântica e tipos       |
| `test_codegen.py`     | 23     | Geração de código, loops reversos |
| `test_integration.py` | 14     | Pipeline completo end-to-end      |
| **TOTAL**             | **98** | **~80% de cobertura**             |

### 🔧 **Fixtures Disponíveis** (`conftest.py`)

```python
@pytest.fixture
def codigo_fibonacci():
    """Retorna código Portugol para sequência Fibonacci"""

@pytest.fixture
def codigo_loop_reverso():
    """Retorna código com loop de passo negativo"""

@pytest.fixture
def codigo_passo_opcional():
    """Retorna código com passo opcional no loop"""
```

### ✅ **Testes Críticos**

**Loop com Passo Negativo:**

```python
def test_execucao_loop_negativo():
    """Testa que loop reverso executa corretamente"""
    codigo = """
    inteiro i, conta;
    inicio
        conta <- 0
        para i de 5 ate 1 passo -1 faca
            conta <- conta + 1
        fimpara
    fim
    """
    compilador = CompiladorPortugol()
    resultado = compilador.executar_compilacao_e_teste(codigo)
    assert resultado is True  # ✅ PASSA (v2.1), FALHAVA (v2.0)
```

**Passo Opcional:**

```python
def test_repeticao_para_sem_passo():
    """Testa loop sem passo explícito (deve usar 1)"""
    codigo = """
    inteiro i;
    inicio
        para i de 1 ate 5 faca
            escreva(i)
        fimpara
    fim
    """
    compilador = CompiladorPortugol()
    resultado = compilador.executar_compilacao_e_teste(codigo)
    assert resultado is True  # ✅ NOVA FEATURE (v2.1)
```

---

## 📊 Métricas do Projeto

| Métrica                      | Valor       |
| ---------------------------- | ----------- |
| **Linhas de Código**         | ~3.500      |
| **Módulos**                  | 10          |
| **Testes**                   | 98          |
| **Cobertura de Testes**      | ~80%        |
| **Fases de Compilação**      | 6           |
| **Otimizações**              | 5 tipos     |
| **Exemplos**                 | 9 programas |
| **Redução Máxima de Código** | 29.7%       |

---

## 🐛 Correções Críticas (v2.0 → v2.1)

### 🔴 **Bug Crítico: Loop com Passo Negativo**

**Problema (v2.0):**

```portugol
para i de 10 ate 1 passo -1 faca
    escreva(i)  // Nunca executava!
fimpara
```

**Causa:** Condição estática `while i <= 1` sempre falsa quando i=10

**Solução (v2.1):** Condição dinâmica que detecta sinal do passo

```python
# Código Python gerado (v2.1)
while ((-1) > 0 and i <= 1) or ((-1) < 0 and i >= 1):
    # Agora funciona corretamente!
```

**Impacto:** Loops reversos, contadores regressivos e algoritmos de backtracking agora funcionam ✅

---

### 🆕 **Nova Feature: Passo Opcional**

**Antes (v2.0):**

```portugol
para i de 1 ate 10 passo 1 faca  // passo obrigatório
    escreva(i)
fimpara
```

**Agora (v2.1):**

```portugol
para i de 1 ate 10 faca  // passo opcional (padrão = 1)
    escreva(i)
fimpara
```

**Benefício:** Código mais limpo e intuitivo para casos comuns

---

## 🛠️ Desenvolvimento

### 🔧 **Estrutura de Código**

```python
# Estrutura típica de um módulo
class AnalisadorLexico:
    """Classe responsável pela análise léxica"""

    def __init__(self, codigo: str):
        self.codigo = codigo
        self.posicao = 0

    def proximo_token(self) -> Token:
        """Retorna o próximo token do código"""
        # Implementação...
```

### 📝 **Convenções**

- **PEP 8:** Código segue padrões Python
- **Type Hints:** Anotações de tipo em funções críticas
- **Docstrings:** Documentação em português
- **Exceções:** Hierarquia customizada (`ErroLexico`, `ErroSintatico`, `ErroSemantico`)

### 🧪 **Executar Testes Durante Desenvolvimento**

```bash
# Executar testes em modo watch
python -m pytest tests/ -v --tb=short

# Executar teste específico
python -m pytest tests/test_parser.py::TestParserComandos::test_repeticao_para_sem_passo -v

# Gerar relatório de cobertura
python -m pytest tests/ --cov=src --cov-report=term-missing
```

---

## 📚 Referências

### 📖 **Bibliografia Acadêmica**

1. **Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D.** (2006). _Compilers: Principles, Techniques, and Tools_ (2nd ed.). Addison-Wesley. (Dragon Book)

2. **Appel, A. W.** (2004). _Modern Compiler Implementation in Java_ (2nd ed.). Cambridge University Press.

3. **Cooper, K. D., & Torczon, L.** (2011). _Engineering a Compiler_ (2nd ed.). Morgan Kaufmann.

### 🔗 **Recursos Online**

- [Python Official Documentation](https://docs.python.org/3/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Regular Expressions 101](https://regex101.com/)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

**Áreas para Contribuição:**

- 🐛 Correção de bugs
- ✨ Novas features de linguagem
- 🧪 Mais testes
- 📚 Melhorias na documentação
- ⚡ Otimizações adicionais

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 Autor

**Erick Vieira**

- GitHub: [@ErickIV](https://github.com/ErickIV)
- Instituição: UNISUL - Universidade do Sul de Santa Catarina

---

## 🙏 Agradecimentos

- Prof. da UC de Teoria da Computação e Compiladores (UNISUL)
- Autores do "Dragon Book" pela base teórica
- Comunidade Python pelo excelente ecossistema de ferramentas
- Contribuidores e testadores do projeto

---

## 📞 Contato e Suporte

- **Issues:** [GitHub Issues](https://github.com/ErickIV/Compilador-de-Portugol/issues)
- **Discussões:** [GitHub Discussions](https://github.com/ErickIV/Compilador-de-Portugol/discussions)

---

<div align="center">

### ⭐ Se este projeto foi útil, considere dar uma estrela!

**Feito com ❤️ para a comunidade educacional**

</div>
