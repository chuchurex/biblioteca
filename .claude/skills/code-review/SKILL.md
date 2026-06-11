---
name: code-review
description: "Automatic code review with quality, security and architecture analysis"
---

# Code Review Command

Performs automatic and comprehensive code reviews using advanced AI analysis to improve quality, security, and maintainability.

## Description

The `/code-review` command provides complete and professional code review using advanced AI to analyze:

- **Code quality** - Complexity, readability, maintainability
- **Architecture and patterns** - Design, organization, structure
- **Performance and optimization** - Bottlenecks, performance improvements
- **Security** - Vulnerabilities, security best practices
- **Testing** - Coverage, test quality, missing cases
- **Documentation** - Comments, JSDoc, clarity
- **Best practices** - Conventions, industry standards
- **Refactoring suggestions** - Specific and actionable improvements

## Usage

```
/code-review [directory] [--aspects] [--severity] [--format] [--depth]
```

### Parámetros

- `directory` (opcional): directory específico a revisar. Por defecto analiza todo el proyecto.
- `--aspects`: Aspectos específicos a revisar (calidad, arquitectura, performance, seguridad, testing, docs)
- `--severity`: Nivel de crítica (strict, moderate, relaxed)
- `--format`: Formato de salida (detailed, summary, actionable, report)
- `--depth`: Nivel de análisis (surface, deep, comprehensive)
- `--contexto`: Contexto del proyecto (startup, enterprise, legacy, greenfield)
- `--tech-stack`: Stack tecnológico (react, vue, node, python, etc.)
- `--focus`: Foco específico (maintainability, scalability, performance, security)

### Examples

```
/code-review
/code-review src/ --aspects=calidad,performance --severity=strict
/code-review components/ --aspects=arquitectura --tech-stack=react
/code-review --format=actionable --depth=comprehensive
/code-review backend/ --focus=security,performance --contexto=enterprise
/code-review src/utils/ --aspects=testing --format=report
```

## Aspectos de Análisis

### 🏗️ Calidad del Código

#### Complejidad y Legibilidad
- Complejidad ciclomática por función
- Profundidad de anidamiento
- Longitud de functions y clases
- Claridad en naming conventions
- Coherencia en el estilo de código

#### Mantenibilidad
- Acoplamiento entre módulos
- Cohesión dentro de clases/módulos
- Principios SOLID
- DRY (Don't Repeat Yourself)
- Facilidad de modificación

### 🏛️ Arquitectura y Patterns

#### Estructura del Proyecto
- Organización de directorys
- Separación de responsabilidades
- Modularidad y encapsulación
- Dependencias y acoplamiento

#### Patterns de Diseño
- Implementación de Patterns apropiados
- Anti-Patterns detectados
- Arquitectura escalable
- Principios de diseño

### ⚡ Performance y Optimización

#### Análisis de Rendimiento
- Algoritmos ineficientes
- Operaciones costosas innecesarias
- Memory leaks potenciales
- Optimizaciones de base de datos

#### Mejores Prácticas de Performance
- Lazy loading opportunities
- Caching strategies
- Bundle optimization
- Resource optimization

### 🔒 Seguridad

#### Vulnerabilidades Comunes
- Injection attacks (SQL, XSS, etc.)
- Authentication/Authorization flaws
- Sensitive data exposure
- Insecure configurations

#### Buenas Prácticas de Seguridad
- Input validation
- Output encoding
- Secure communication
- Error handling seguro

### 🧪 Testing

#### Cobertura y Calidad
- Porcentaje de cobertura
- Tipos de tests necesarios
- Calidad de assertions
- Edge cases coverage

#### Estrategia de Testing
- Unit tests appropriateness
- Integration tests needs
- E2E testing gaps
- Test maintainability

### 📚 Documentación

#### Documentación del Código
- Comentarios útiles vs noise
- JSDoc/docstrings completeness
- API documentation
- Code self-documentation

#### Documentación del Proyecto
- README completeness
- Setup instructions
- Architecture documentation
- Contributing guidelines

## Configuración

El comando utiliza `.claude/code-review-config.json`:

```json
{
  "severity": "moderate",
  "aspects": {
    "quality": {
      "enabled": true,
      "weight": 25,
      "thresholds": {
        "cyclomaticComplexity": 10,
        "functionLength": 50,
        "nestingDepth": 4,
        "duplicateLines": 5
      }
    },
    "architecture": {
      "enabled": true,
      "weight": 20,
      "patterns": ["mvc", "component", "service", "repository"],
      "antiPatterns": ["god-object", "spaghetti", "golden-hammer"]
    },
    "performance": {
      "enabled": true,
      "weight": 20,
      "focus": ["algorithms", "memory", "io", "rendering"]
    },
    "security": {
      "enabled": true,
      "weight": 25,
      "standards": ["owasp-top10", "cwe-top25"],
      "scanTypes": ["static", "dependency", "configuration"]
    },
    "testing": {
      "enabled": true,
      "weight": 15,
      "targetCoverage": 80,
      "requiredTypes": ["unit", "integration"]
    },
    "documentation": {
      "enabled": true,
      "weight": 10,
      "requireApiDocs": true,
      "minCommentRatio": 0.1
    }
  },
  "contextSettings": {
    "startup": {
      "focus": ["speed", "mvp", "flexibility"],
      "relaxedStandards": ["documentation", "comprehensive-testing"]
    },
    "enterprise": {
      "focus": ["security", "maintainability", "scalability"],
      "strictStandards": ["all"]
    },
    "legacy": {
      "focus": ["refactoring", "testing", "documentation"],
      "graduatedApproach": true
    }
  }
}
```

## Salida del Comando

### Resumen Ejecutivo
```
👨‍💻 CLAUDE POWER - CODE REVIEW REPORT
=====================================

📊 PUNTUACIÓN GENERAL: 8.2/10 (BUENO)
⏱️ Análisis completado en 45.3s - 127 files revisados

🎯 ASPECTOS EVALUADOS:
┌─────────────────┬───────┬─────────┬─────────────┐
│ Aspecto         │ Score │ Weight  │ Impacto     │
├─────────────────┼───────┼─────────┼─────────────┤
│ Calidad         │  8.5  │  25%    │ Excelente   │
│ Arquitectura    │  7.8  │  20%    │ Bueno       │
│ Performance     │  9.1  │  20%    │ Excelente   │
│ Seguridad       │  7.2  │  25%    │ Bueno       │
│ Testing         │  7.9  │  15%    │ Bueno       │
│ Documentación   │  6.8  │  10%    │ Necesita ♻️ │
└─────────────────┴───────┴─────────┴─────────────┘

🚦 ESTADO GENERAL: ✅ APROBADO CON SUGERENCIAS
```

### Análisis Detallado por Aspecto

```
🏗️ CALIDAD DEL CÓDIGO (8.5/10)
==============================

✅ FORTALEZAS:
• functions bien dimensionadas (promedium: 28 líneas)
• Naming conventions consistentes
• low acoplamiento entre módulos
• DRY principles bien aplicados

⚠️ ÁREAS DE MEJORA:
• 3 functions con alta complejidad ciclomática (>10)
• Algunos méall anidados profundamente (>4 niveles)
• Inconsistencias menores en formateo

📁 files CON ISSUES:
src/utils/dataProcessor.js (Línea 45-67)
  🔴 CRÍTICO: Función processComplexData() demasiado compleja (CC: 15)
  💡 SUGERENCIA: Extraer sub-functions para validateData(), transformData(), formatResult()

src/components/Dashboard.tsx (Línea 120-145)
  🟡 moderate: Anidamiento profundo en renderWidgets()
  💡 SUGERENCIA: Usar early returns o component extraction

🏛️ ARQUITECTURA Y Patterns (7.8/10)
===================================

✅ FORTALEZAS:
• Clara separación de concerns
• Buen uso de composition over inheritance
• Modularidad apropiada
• Dependency injection bien implementada

⚠️ ÁREAS DE MEJORA:
• Algunos componentes violan Single Responsibility
• Falta abstracciones para operaciones complejas
• Inconsistencias en error handling patterns

📁 PROBLEMAS DETECTADOS:
src/services/ApiService.js
  🔴 ANTI-PATTERN: God Object detectado (12 responsabilidades)
  💡 SUGERENCIA: Dividir en UserApiService, ProductApiService, OrderApiService

src/components/UserProfile.tsx
  🟡 VIOLACIÓN SRP: Maneja UI, validación y API calls
  💡 SUGERENCIA: Extraer useUserValidation hook y userApi service

⚡ PERFORMANCE Y OPTIMIZACIÓN (9.1/10)
=====================================

✅ FORTALEZAS:
• Excelente uso de memoization
• Lazy loading implementado correctamente
• Bundle splitting apropiado
• Queries optimizadas

⚠️ OPORTUNIDADES DE MEJORA:
• 2 loops innecesarios en data processing
• Algunos re-renders evitables

📁 OPTIMIZACIONES SUGERIDAS:
src/hooks/useDataFetching.ts
  🟡 MEJORA: Implementar caching con React Query
  💡 IMPACTO: -40% API calls, +60% perceived performance

src/utils/calculations.js
  🟡 OPTIMIZACIÓN: Replace O(n²) algorithm with O(n log n)
  💡 IMPACTO: -85% execution time para datasets grandes

🔒 SEGURIDAD (7.2/10)
====================

✅ FORTALEZAS:
• Input validation implementada
• HTTPS enforced
• Secrets externalizados
• CORS configurado correctamente

🚨 VULNERABILIDADES DETECTADAS:
src/components/CommentForm.tsx
  🔴 XSS RISK: User input no sanitizado antes de render
  💡 FIX: Usar DOMPurify o built-in sanitization

src/api/userEndpoints.js
  🟡 SQL INJECTION: Query building sin prepared statements
  💡 FIX: Implementar parameterized queries

🧪 TESTING (7.9/10)
==================

✅ FORTALEZAS:
• Cobertura general: 87% (target: 80%)
• Buenos unit tests para utils
• E2E tests para flujos críticos

⚠️ GAPS IDENTIFICADOS:
• 5 componentes sin tests unitarios
• Falta integration tests para API layer
• Edge cases no cubiertos en validations

📁 TESTS FALTANTES:
src/components/PaymentForm.tsx
  🔴 CRÍTICO: Componente crítico sin tests
  💡 PRIORIDAD: Unit tests + E2E para flujo de pago

src/services/PaymentService.js
  🟡 IMPORTANTE: Solo happy path testeado
  💡 AGREGAR: Error handling, timeout, retry scenarios
```

### Sugerencias Actionables

```
🛠️ PLAN DE ACCIÓN RECOMENDADO:
=============================

🔴 ALTA PRIORIDAD (Fix inmediato):
1. Corregir vulnerabilidad XSS en CommentForm.tsx
2. Implementar prepared statements en userEndpoints.js
3. Agregar tests para PaymentForm.tsx
4. Refactorizar función processComplexData() (alta complejidad)

🟡 MEDIA PRIORIDAD (Próximo sprint):
5. Dividir ApiService en servicios específicos
6. Extraer hooks de UserProfile.tsx
7. Implementar caching en useDataFetching
8. Agregar integration tests para API layer

🟢 BAJA PRIORIDAD (Backlog):
9. Mejorar documentación de componentes
10. Optimizar algoritmo en calculations.js
11. Standardizar error handling patterns
12. Incrementar cobertura de edge cases

⏱️ ESTIMACIÓN TOTAL: 18-25 días desarrollo
💰 IMPACTO BUSINESS: high (security + performance)
```

### Métricas de Calidad

```
📈 TENDENCIAS Y MÉTRICAS:
========================

📊 EVOLUCIÓN (vs último review):
• Calidad general: +0.7 puntos 📈
• Cobertura tests: +12% 📈  
• Vulnerabilidades: -2 issues 📈
• Complejidad promedium: +0.3 📊
• Documentación: -0.2 puntos 📉

🎯 BENCHMARKS INDUSTRIA:
• Nuestro score: 8.2/10
• Promedium industria: 7.4/10
• Top 10% empresas: 8.8/10
• Objetivo Q4: 8.5/10

🏆 ACHIEVEMENTS:
• ✅ Zero critical vulnerabilities (por 3er mes)
• ✅ >85% test coverage mantenido
• ✅ <10 avg cyclomatic complexity
• ⚠️ Documentation coverage: 68% (target: 75%)
```

## Integración con Workflow

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔍 Running code review analysis..."
REVIEW_RESULT=$(npx claude-power code-review --format=summary --aspects=security,quality)

if echo "$REVIEW_RESULT" | grep -q "CRÍTICO"; then
  echo "❌ Critical issues found. Please fix before committing:"
  echo "$REVIEW_RESULT"
  exit 1
fi

echo "✅ Code review passed"
```

### CI/CD Pipeline
```yaml
name: Code Review

on:
  pull_request:
    branches: [main, develop]

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Run comprehensive code review
        run: |
          npx claude-power code-review \
            --format=report \
            --depth=comprehensive \
            --output=json > review-report.json
            
      - name: Comment PR with review
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const review = JSON.parse(fs.readFileSync('review-report.json'));
            
            const comment = `
            ## 👨‍💻 Automated Code Review
            
            **Overall Score:** ${review.overall_score}/10
            
            ### 🎯 Key Findings:
            ${review.key_findings.map(f => `- ${f}`).join('\n')}
            
            ### 🚨 Critical Issues:
            ${review.critical_issues.length} found
            
            ### 💡 Recommendations:
            ${review.top_recommendations.slice(0, 3).map(r => `- ${r}`).join('\n')}
            
            [View full report](${review.report_url})
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### VS Code Integration
```json
{
  "tasks": [
    {
      "label": "Code Review - Quick",
      "type": "shell",
      "command": "npx",
      "args": [
        "claude-power",
        "code-review",
        "${file}",
        "--format=summary"
      ],
      "group": "build"
    },
    {
      "label": "Code Review - Comprehensive", 
      "type": "shell",
      "command": "npx",
      "args": [
        "claude-power",
        "code-review",
        "--depth=comprehensive",
        "--format=detailed"
      ],
      "group": "build"
    }
  ]
}
```

---

*Parte del ecosistema **Claude Power** - Eleva la calidad de tu código con IA* 🚀 
