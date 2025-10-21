# Compilador Portugol - AI Coding Instructions

## Architecture Overview

This is a **4-phase educational compiler** translating Portugol (Portuguese pseudocode) to executable Python. Each phase is strictly isolated in separate modules following classic compiler architecture:

```
Source Code (.por) → Lexer → Parser → Semantic Analyzer → Code Generator → Python
```

**Critical Design Principle**: The pipeline is **unidirectional and immutable**. Each phase consumes the output of the previous phase without back-propagation. No phase modifies inputs from prior phases.

## Module Responsibilities

### 1. `lexer.py` - Tokenization Phase
- **Input**: Raw source string
- **Output**: Stream of `Token` objects with position tracking
- **State Management**: Maintains `linha` (line) and `coluna` (column) for error reporting
- **Comment Handling**: Ignores `//` line comments and `/* */` block comments
- **Pattern**: Uses `palavras_chave` dict to distinguish keywords from identifiers

### 2. `parser.py` - Syntax Analysis
- **Input**: `Lexer` instance
- **Output**: `Programa` AST node with `declaracoes` and `comandos`
- **Pattern**: Recursive descent parser with `_esperar_token()` for syntax validation
- **Grammar Structure**: 
  - Variables must be declared before `inicio` keyword
  - All commands between `inicio` and `fim`
  - Program ends with `EOF` token

### 3. `semantic.py` - Type/Scope Validation
- **Input**: `Programa` AST
- **Output**: Validated AST (modifies in-place via `TabelaSimbolos`)
- **Key Checks**:
  - Variable declaration before use
  - Type compatibility in operations (via `_verificar_tipos_compativeis()`)
  - Uninitialized variable warnings (not errors)
- **Pattern**: Uses visitor pattern on AST nodes

### 4. `codegen.py` - Python Generation
- **Input**: Validated `Programa` AST
- **Output**: Executable Python string
- **Type Mapping**: `inteiro→int`, `real→float`, `caracter→str`, `logico→bool`
- **Pattern**: 
  - Wraps everything in `main()` function
  - Uses `nivel_indentacao` for proper Python indentation
  - Initializes all variables with defaults before commands

## Critical Workflows

### Compiling & Running Programs
```bash
# Standard execution (compile + run)
python compilar.py programa.por

# Debug mode (shows all 4 phases)
python compilar.py programa.por --debug

# Save generated Python (doesn't execute)
python compilar.py programa.por --save
```

**Important**: `compilar.py` is the CLI entry point. It calls `src/main.py::CompiladorPortugol` which orchestrates the pipeline. Never bypass the main compiler class.

### Adding New Language Features

**Always follow this order**:
1. Add token type to `TipoToken` enum in `ast_nodes.py`
2. Update `palavras_chave` dict in `lexer.py` (if keyword)
3. Create AST node class in `ast_nodes.py` (inherit from `Comando` or `Expressao`)
4. Implement parsing logic in `parser.py` (add to `_analisar_comando()` or expression parser)
5. Add semantic validation in `semantic.py` (add visitor method)
6. Implement code generation in `codegen.py` (add to `_gerar_comando()`)

### Error Handling Convention

Use custom exceptions from `exceptions.py`:
- `ErroLexico` - Invalid characters/tokens
- `ErroSintatico` - Grammar violations  
- `ErroSemantico` - Type/scope issues
- `ErroGeracaoCodigo` - Code generation failures

**Pattern**: All exceptions include `linha` and `coluna` for precise error location.

## Language-Specific Patterns

### Portugol Syntax Rules
- **Assignment**: Uses `<-` not `=` (e.g., `x <- 10`)
- **Logic Operators**: Portuguese keywords `e` (and), `ou` (or)
- **Booleans**: `verdadeiro`/`falso` not true/false
- **I/O**: `leia(var)` for input, `escreva(expr, ...)` for output
- **Structure Keywords**: `entao`/`senao`/`fimse`, `faca`/`fimenquanto`

### Type System
Portugol is **weakly typed** - variables declared with types but no runtime type checking. The semantic analyzer validates compatibility but allows implicit conversions in Python generation.

## Testing & Examples

- `exemplos/demo_completa.por` - Non-interactive test suite (all features, 2-second run)
- `exemplos/calculadora_imc.por` - Interactive user input example
- `exemplos/bubble_sort.por` - Algorithm with nested loops

**Test Pattern**: Always test with `demo_completa.por` first after changes - it exercises all language features.

## Common Pitfalls

1. **Token Lookahead**: Parser uses `self.token_atual` for current token, advance with `_avancar()` not `_esperar_token()`
2. **Indentation**: Code generator tracks indentation state - never emit raw strings with tabs/spaces, use `_adicionar_linha()`
3. **Variable Scope**: Portugol has single global scope - no nested scopes or functions
4. **Comment Position**: Comments can appear anywhere in lexer, must be consumed before tokenizing next token
5. **EOF Handling**: Parser expects explicit `TipoToken.EOF` - lexer must emit this after last token

## Dependencies & Environment

- **Pure Python**: No external dependencies, uses only stdlib
- **Python Version**: Requires 3.11+ for dataclasses and typing features
- **Encoding**: All `.por` files are UTF-8 (important for Portuguese characters)
- **Shell**: CLI designed for PowerShell on Windows (uses `;` for command chaining)
