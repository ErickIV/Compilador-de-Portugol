# Exemplos de Programas em Portugol

Esta pasta contém programas de exemplo para demonstração do compilador Portugol.

## Programas Disponíveis

### 1. **demo_completa.por** 
**Recomendado para apresentação rápida em sala de aula**

Demonstra TODAS as funcionalidades do compilador em um único programa:
- ✅ Todos os tipos de dados (inteiro, real, caracter, logico)
- ✅ Operações aritméticas (+, -, *, /)
- ✅ Operadores relacionais (<, <=, >, >=, ==, !=)
- ✅ Operadores lógicos (e, ou)
- ✅ Estruturas condicionais (se-entao-senao)
- ✅ Loops (enquanto-faca)
- ✅ Expressões complexas
- ✅ Cálculos matemáticos

**Execução:** `python compilar.py exemplos/demo_completa.por`

**Tempo de execução:** ~2 segundos (não requer entrada do usuário)

---

### 2. **calculadora_imc.por**
**Melhor para demonstrar interatividade e lógica complexa**

Calculadora completa de IMC com:
- 📥 Entrada de dados do usuário (leia)
- 🧮 Cálculos matemáticos complexos
- 🌳 Condicionais aninhadas (múltiplos níveis)
- ✅ Validação de entrada
- 📊 Classificação por faixas (IMC e idade)
- 💡 Recomendações personalizadas

**Execução:** `python compilar.py exemplos/calculadora_imc.por`

**Tempo de execução:** ~30 segundos (com entrada do usuário)

**Entradas de exemplo:**
- Nome: João
- Idade: 25
- Altura: 1.75
- Peso: 70

---

### 3. **bubble_sort.por**
**Melhor para demonstrar algoritmos e loops complexos**

Implementação do algoritmo Bubble Sort com:
- 🔄 Loops aninhados (enquanto dentro de enquanto)
- 🔢 Múltiplas variáveis e contadores
- 🔄 Troca de valores entre variáveis
- 📊 Estatísticas de execução
- 💡 Análise de complexidade

**Execução:** `python compilar.py exemplos/bubble_sort.por`

**Tempo de execução:** ~45 segundos (com entrada do usuário)

**Entradas de exemplo:**
- Números: 5, 2, 8, 1, 9 (para ver muitas trocas)
- Números: 1, 2, 3, 4, 5 (para ver otimização)

---

### 4. **teste_otimizacoes.por** [NOVO]
**Melhor para demonstrar código intermediário e otimizações**

Demonstração das 5 otimizações implementadas:
- ⚡ Constant Folding (dobramento de constantes)
- ⚡ Constant Propagation (propagação de constantes)
- ⚡ Algebraic Simplification (simplificação algébrica)
- ⚡ Copy Propagation (propagação de cópias)
- ⚡ Dead Code Elimination (código morto)

**Execução Normal:** `python compilar.py exemplos/teste_otimizacoes.por`

**Com Otimizações:** `python compilar.py exemplos/teste_otimizacoes.por --intermediate --optimize`

**Tempo de execução:** ~1 segundo

**Mostra:**
- Código intermediário original (37 instruções)
- Código intermediário otimizado (26 instruções)
- Redução de 29.7% no código gerado

---

## Como Executar

### Execução Normal
```bash
python compilar.py exemplos/demo_completa.por
```

### Com Debug (mostra fases da compilação)
```bash
python compilar.py exemplos/demo_completa.por --debug
```

### Salvar código Python gerado
```bash
python compilar.py exemplos/demo_completa.por --save
```

### Mostrar código intermediário e otimizações [NOVO]
```bash
python compilar.py exemplos/teste_otimizacoes.por --intermediate --optimize
```

### Demonstrar AFDs (educacional) [NOVO]
```bash
python compilar.py exemplos/demo_completa.por --show-afd
```

---

## Sugestão para Apresentação

### Roteiro Recomendado (15-20 minutos)

1. **Introdução (2 min)**
   - Explicar o que é o compilador Portugol
   - Mostrar a estrutura do projeto (`src/`)

2. **Demo Rápida (5 min)**
   - Executar `demo_completa.por` com `--debug`
   - Mostrar as 4 fases da compilação
   - Explicar cada fase brevemente

3. **Programa Interativo (5 min)**
   - Executar `calculadora_imc.por`
   - Demonstrar entrada de dados
   - Mostrar validações e lógica complexa

4. **Algoritmo (5 min)**
   - Executar `bubble_sort.por`
   - Explicar o algoritmo visualmente
   - Mostrar estatísticas e otimizações

5. **Perguntas (3-5 min)**

---

## Recursos Técnicos

- **Linguagem de Implementação:** Python 3.11+
- **Paradigma:** Compilador modular de 6 fases
- **Fases:**
  1. Análise Léxica (Lexer) + Expressões Regulares
  2. Análise Sintática (Parser) + AFDs
  3. Análise Semântica (Semantic)
  4. Geração de Código Intermediário (Intermediate) [Opcional]
  5. Otimização (Optimizer) [Opcional]
  6. Geração de Código Final (CodeGen)

- **Saída:** Código Python executável otimizado
- **Otimizações:** 5 tipos implementados
- **AFDs:** 3 autômatos educacionais
