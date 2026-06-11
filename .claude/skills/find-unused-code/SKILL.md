---
name: find-unused-code
description: "Detects unused code, variables, functions and imports in the project"
---

# Find Unused Code Command

Detects code, variables, functions, imports, and files that are not used in the project.

## Description

The `/find-unused-code` command performs deep project analysis to identify:

- Variables declared but not used
- Functions defined but never called
- Imports not referenced in code
- Exports without external references
- Unused React components
- Files completely without references
- CSS classes and styles not applied
- Unused package.json dependencies
- Object properties not accessed
- Function parameters not used

## Usage

```
/find-unused-code [directory] [--types] [--severity] [--include]
```

### Parámetros

- `directory` (opcional): directory específico a analizar. Por defecto analiza todo el proyecto.
- `--types`: Tipos específicos a buscar (variables, functions, imports, exports, files, css, deps)
- `--severity`: Nivel de impacto (high, medium, low, all)
- `--include`: Incluir categorías específicas (test-files, node-modules, config-files)
- `--exclude-patterns`: Patterns de files a excluir
- `--min-size`: Tamaño mínimo de código para considerar (en líneas)

### Examples

```
/find-unused-code
/find-unused-code src/ --types=variables,functions
/find-unused-code --types=imports --severity=high
/find-unused-code components/ --types=react --include=test-files
/find-unused-code --types=deps --severity=high
/find-unused-code styles/ --types=css
```

## Patterns Detectados

### Variables No Utilizadas
- Variables declaradas con let, const, var sin uso
- Destructuring assignments no utilizados
- Loop variables no usadas
- Parameters de función no utilizados

### functions No Utilizadas
- functions declaradas pero nunca llamadas
- Arrow functions sin referencias
- Méall de clase no invocados
- Callbacks no utilizados

### Imports/Exports No Utilizados
- Import statements sin uso en el código
- Default imports no referenciados
- Named imports sin uso
- Exports que no se importan en ningún lugar
- Re-exports innecesarios

### Componentes React
- Componentes definidos pero nunca renderizados
- Hooks personalizados sin uso
- Contexts no utilizados
- Higher-Order Components sin referencias

### files Sin Referencias
- files TypeScript/JavaScript no importados
- Componentes no utilizados en ningún lugar
- Utilities sin referencias
- files de configuración obsoletos

### CSS/Estilos
- Classes CSS no aplicadas en JSX/HTML
- IDs no referenciados
- Selectores sin uso
- Variables CSS no utilizadas
- Keyframes no aplicados

### Dependencias
- Packages en package.json no importados
- DevDependencies no utilizadas en scripts
- Peer dependencies innecesarias

## Configuración

El comando utiliza `.claude/find-unused-code-config.json`:

```json
{
  "severity": "medium",
  "analysis": {
    "variables": true,
    "functions": true,
    "imports": true,
    "exports": true,
    "files": true,
    "css": true,
    "dependencies": true,
    "react": true
  },
  "thresholds": {
    "minFileSize": 5,
    "minFunctionSize": 2,
    "maxUnusedPercentage": 20
  },
  "exclude": [
    "node_modules",
    "dist",
    "build",
    "coverage",
    "*.test.*",
    "*.spec.*",
    "*.d.ts",
    ".git"
  ],
  "include": [
    "**/*.js",
    "**/*.ts",
    "**/*.jsx",
    "**/*.tsx",
    "**/*.css",
    "**/*.scss",
    "**/*.vue"
  ],
  "specialPatterns": {
    "testFiles": ["*.test.*", "*.spec.*", "__tests__/**"],
    "configFiles": ["*.config.*", ".*rc.*", "*.setup.*"],
    "typeFiles": ["*.d.ts", "types/**"]
  },
  "ignorePatterns": [
    "console\\.(log|warn|error)",
    "process\\.env\\.",
    "window\\.",
    "document\\.",
    "__dirname",
    "__filename"
  ]
}
```

## Salida

### Resumen Ejecutivo
```
🧹 CLAUDE POWER - UNUSED CODE REPORT
====================================

📊 RESUMEN:
┌─────────────────┬───────┬─────────┐
│ Categoría       │ Count │ Tamaño  │
├─────────────────┼───────┼─────────┤
│ Variables       │  15   │ 45 LOC  │
│ functions       │   8   │ 120 LOC │
│ Imports         │  23   │ 23 LOC  │
│ files        │   5   │ 340 LOC │
│ CSS Classes     │  12   │ 60 LOC  │
│ Dependencies    │   3   │ N/A     │
│ Total           │  66   │ 588 LOC │
└─────────────────┴───────┴─────────┘

💾 IMPACTO POTENCIAL:
• Reducción de bundle: ~45KB
• files eliminables: 5
• Limpieza estimada: 588 líneas
```

### Detalles por Categoría

```
🔍 VARIABLES NO UTILIZADAS (15):

📁 src/components/UserProfile.tsx
  💡 [medium] Línea 12: const unusedVariable = getData()
     > Declarada pero nunca referenciada
     💾 Impacto: 1 línea

  💡 [low] Línea 25: const { name, ...unused } = props
     > Destructuring no utilizado
     💾 Impacto: 1 línea

📁 src/utils/helpers.js
  ⚠️ [high] Línea 5: function calculateTotal(items) { ... }
     > Función completa sin uso (15 líneas)
     💾 Impacto: 15 líneas

🔍 IMPORTS NO UTILIZADOS (23):

📁 src/components/Dashboard.tsx
  💡 [medium] Línea 3: import { useState } from 'react'
     > Hook importado pero no utilizado
     
  💡 [medium] Línea 5: import lodash from 'lodash'
     > Librería importada sin uso

🔍 files SIN REFERENCIAS (5):

📁 src/components/OldButton.tsx (68 líneas)
  ❌ [high] Archivo completo sin imports ni referencias
     > Componente React no utilizado en ningún lugar
     💾 Impacto: 68 líneas + eliminación segura
     
📁 src/utils/deprecated.js (95 líneas)
  ❌ [high] Utilidades legacy sin referencias
     💾 Impacto: 95 líneas + eliminación segura

🔍 CSS NO UTILIZADO (12):

📁 src/styles/components.css
  💡 [medium] .unused-button-style { ... }
     > Class CSS no aplicada en JSX
     
  💡 [low] #unique-id { ... }
     > ID selector sin referencias en HTML/JSX

🔍 DEPENDENCIAS NO UTILIZADAS (3):

📁 package.json
  ⚠️ [high] "moment": "^2.29.4"
     > Dependencia no importada en ningún archivo
     💾 Impacto: ~67KB en bundle
     
  💡 [medium] "uuid": "^9.0.0"
     > Utilizada solo en tests, mover a devDependencies
```

### Sugerencias de Limpieza

```
🛠️ ACCIONES RECOMENDADAS:

🟢 SEGURAS (Auto-aplicables):
• Remover 15 variables no utilizadas
• Eliminar 23 imports innecesarios  
• Limpiar 12 CSS rules sin uso

🟡 REVISAR MANUALMENTE:
• 5 files sin referencias (verificar si son entry points)
• 3 dependencias no utilizadas (verificar uso en build/config)
• 8 functions sin llamadas directas (pueden ser exports públicos)

🔴 REQUIERE ATENCIÓN:
• src/components/OldButton.tsx - Posible feature legacy
• moment dependency - 67KB de impacto en bundle

⚡ COMANDOS SUGERIDOS:
/fix-unused --auto --types=variables,imports
/remove-files --confirm --files=src/components/OldButton.tsx
npm uninstall moment uuid && npm install --save-dev uuid
```

## Integración y Automatización

### CI/CD Pipeline
```yaml
# .github/workflows/cleanup.yml
- name: Detect unused code
  run: |
    npx claude-power find-unused-code --output=json > unused.json
    UNUSED_COUNT=$(jq '.summary.total' unused.json)
    if [ $UNUSED_COUNT -gt 50 ]; then
      echo "⚠️ High amount of unused code detected: $UNUSED_COUNT items"
      # Optional: fail build or create PR comment
    fi
```

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit
UNUSED=$(npx claude-power find-unused-code --severity=high --types=variables,imports)
if [ $? -eq 0 ] && [ ! -z "$UNUSED" ]; then
  echo "⚠️ Unused code detected. Run cleanup before commit:"
  echo "$UNUSED"
fi
```

### VS Code Task
```json
{
  "tasks": [
    {
      "label": "Find Unused Code",
      "type": "shell",
      "command": "npx claude-power find-unused-code ${workspaceFolder}",
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always"
      }
    }
  ]
}
```

## Casos de Uso Avanzados

### Análisis de Bundle Size
```bash
# Detectar código no usado que impacta el bundle
/find-unused-code --types=deps,imports --severity=high --output=json
```

### Limpieza de Legacy Code
```bash
# Encontrar files y functions de features antiguas
/find-unused-code src/legacy/ --types=files,functions --min-size=10
```

### Optimización de CSS
```bash
# Detectar estilos no utilizados en componentes
/find-unused-code styles/ --types=css --include=components
```

### Análisis de Test Coverage
```bash
# Encontrar código de tests no utilizado
/find-unused-code tests/ --include=test-files --types=functions
```

---

*Parte del ecosistema **Claude Power** - Potenciando el desarrollo con IA* 🚀 
