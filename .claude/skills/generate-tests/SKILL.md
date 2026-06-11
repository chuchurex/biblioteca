---
name: generate-tests
description: "Generates comprehensive automatic tests to maximize coverage"
---

# Generate Tests Command

Automatically generates comprehensive tests using advanced AI to maximize coverage, quality and edge cases with minimal effort.

## Description

The `/generate-tests` command revolutionizes test writing by completely automating the process:

- **Automatic generation** of unit, integration and E2E tests
- **Code analysis** to identify all necessary test cases
- **Automatic edge cases** that humans often forget
- **Intelligent mocks** for external dependencies
- **Optimized coverage** to reach desired metrics
- **Multiple frameworks** (Jest, Vitest, Cypress, Playwright, etc.)
- **Best practices patterns** in testing built-in
- **Maintainable tests** with clear naming and logical structure

## Usage

```
/generate-tests [file/directory] [--type] [--framework] [--coverage] [--mocks]
```

### Parameters

- `file/directory`: Source code for which to generate tests
- `--type`: Types of tests (unit, integration, e2e, performance, accessibility)
- `--framework`: Testing framework (jest, vitest, cypress, playwright, mocha)
- `--coverage`: Coverage target (80%, 90%, 95%)
- `--mocks`: Mocking strategy (auto, manual, none)
- `--patterns`: Testing patterns (aaa, bdd, tdd)
- `--edge-cases`: Edge cases level (basic, comprehensive, paranoid)
- `--performance`: Include performance tests
- `--accessibility`: Include accessibility tests

### Examples

```
/generate-tests src/components/UserProfile.tsx
/generate-tests --type=unit,integration --coverage=95%
/generate-tests api/ --framework=jest --mocks=auto
/generate-tests --edge-cases=comprehensive --patterns=bdd
/generate-tests frontend/ --type=e2e --framework=playwright
/generate-tests utils/ --performance=true --coverage=100%
```

## Generated Test Types

### 🧪 Unit Tests
```javascript
// Auto-generado para UserProfile.tsx
describe('UserProfile Component', () => {
  const mockUser = {
    id: '123',
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'https://example.com/avatar.jpg'
  };

  beforeEach(() => {
    render(<UserProfile user={mockUser} />);
  });

  describe('Rendering', () => {
    it('should render user name correctly', () => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });

    it('should render user email correctly', () => {
      expect(screen.getByText('john@example.com')).toBeInTheDocument();
    });

    it('should render avatar with correct src', () => {
      const avatar = screen.getByAltText('John Doe avatar');
      expect(avatar).toHaveAttribute('src', 'https://example.com/avatar.jpg');
    });
  });

  describe('Edge Cases', () => {
    it('should handle missing avatar gracefully', () => {
      const userWithoutAvatar = { ...mockUser, avatar: null };
      render(<UserProfile user={userWithoutAvatar} />);
      expect(screen.getByText('JD')).toBeInTheDocument(); // Initials fallback
    });

    it('should handle extremely long names', () => {
      const userWithLongName = { 
        ...mockUser, 
        name: 'A'.repeat(100) 
      };
      render(<UserProfile user={userWithLongName} />);
      expect(screen.getByText(/A{50}\.\.\.$/)).toBeInTheDocument(); // Truncated
    });

    it('should handle special characters in name', () => {
      const userWithSpecialChars = { 
        ...mockUser, 
        name: 'José María Aznar-López' 
      };
      render(<UserProfile user={userWithSpecialChars} />);
      expect(screen.getByText('José María Aznar-López')).toBeInTheDocument();
    });
  });

  describe('Interactions', () => {
    it('should call onEdit when edit button is clicked', () => {
      const mockOnEdit = jest.fn();
      render(<UserProfile user={mockUser} onEdit={mockOnEdit} />);
      
      fireEvent.click(screen.getByRole('button', { name: /edit/i }));
      expect(mockOnEdit).toHaveBeenCalledWith(mockUser.id);
    });

    it('should handle rapid multiple clicks gracefully', () => {
      const mockOnEdit = jest.fn();
      render(<UserProfile user={mockUser} onEdit={mockOnEdit} />);
      
      const editButton = screen.getByRole('button', { name: /edit/i });
      fireEvent.click(editButton);
      fireEvent.click(editButton);
      fireEvent.click(editButton);
      
      expect(mockOnEdit).toHaveBeenCalledTimes(1); // Debounced
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      render(<UserProfile user={mockUser} />);
      expect(screen.getByRole('img')).toHaveAttribute('alt', 'John Doe avatar');
      expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
    });

    it('should be keyboard navigable', () => {
      render(<UserProfile user={mockUser} />);
      const editButton = screen.getByRole('button', { name: /edit/i });
      expect(editButton).toHaveAttribute('tabIndex', '0');
    });
  });

  describe('Performance', () => {
    it('should render within performance budget', async () => {
      const start = performance.now();
      render(<UserProfile user={mockUser} />);
      const end = performance.now();
      
      expect(end - start).toBeLessThan(16); // 60fps budget
    });

    it('should not cause memory leaks', () => {
      const { unmount } = render(<UserProfile user={mockUser} />);
      unmount();
      // Verificar que no hay listeners activos
    });
  });
});
```

### 🔗 Integration Tests
```javascript
// Auto-generado para UserService integration
describe('UserService Integration', () => {
  let userService;
  let mockApiClient;

  beforeEach(() => {
    mockApiClient = {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn()
    };
    userService = new UserService(mockApiClient);
  });

  describe('User CRUD Operations', () => {
    it('should fetch user by id successfully', async () => {
      const mockUser = { id: '123', name: 'John Doe' };
      mockApiClient.get.mockResolvedValue({ data: mockUser });

      const result = await userService.getUserById('123');

      expect(mockApiClient.get).toHaveBeenCalledWith('/users/123');
      expect(result).toEqual(mockUser);
    });

    it('should handle network errors gracefully', async () => {
      mockApiClient.get.mockRejectedValue(new Error('Network Error'));

      await expect(userService.getUserById('123')).rejects.toThrow('Failed to fetch user');
    });

    it('should retry failed requests with exponential backoff', async () => {
      mockApiClient.get
        .mockRejectedValueOnce(new Error('500'))
        .mockRejectedValueOnce(new Error('500'))
        .mockResolvedValue({ data: { id: '123' } });

      const result = await userService.getUserById('123');

      expect(mockApiClient.get).toHaveBeenCalledTimes(3);
      expect(result).toEqual({ id: '123' });
    });
  });

  describe('Caching Behavior', () => {
    it('should cache successful responses', async () => {
      const mockUser = { id: '123', name: 'John Doe' };
      mockApiClient.get.mockResolvedValue({ data: mockUser });

      await userService.getUserById('123');
      await userService.getUserById('123');

      expect(mockApiClient.get).toHaveBeenCalledTimes(1);
    });

    it('should invalidate cache after TTL', async () => {
      jest.useFakeTimers();
      const mockUser = { id: '123', name: 'John Doe' };
      mockApiClient.get.mockResolvedValue({ data: mockUser });

      await userService.getUserById('123');
      jest.advanceTimersByTime(300000); // 5 minutes
      await userService.getUserById('123');

      expect(mockApiClient.get).toHaveBeenCalledTimes(2);
      jest.useRealTimers();
    });
  });
});
```

### 🌐 E2E Tests
```javascript
// Auto-generado con Playwright
describe('User Management E2E', () => {
  test('complete user registration flow', async ({ page }) => {
    // Navigate to registration
    await page.goto('/register');
    
    // Fill registration form
    await page.fill('[data-testid="email"]', 'test@example.com');
    await page.fill('[data-testid="password"]', 'SecurePass123!');
    await page.fill('[data-testid="confirmPassword"]', 'SecurePass123!');
    
    // Submit form
    await page.click('[data-testid="submit"]');
    
    // Verify email verification screen
    await expect(page.locator('h1')).toContainText('Check your email');
    
    // Simulate email verification click
    await page.goto('/verify-email?token=mock-token');
    
    // Verify successful registration
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome to the platform!');
  });

  test('handles registration errors gracefully', async ({ page }) => {
    await page.goto('/register');
    
    // Try to register with existing email
    await page.fill('[data-testid="email"]', 'existing@example.com');
    await page.fill('[data-testid="password"]', 'SecurePass123!');
    await page.fill('[data-testid="confirmPassword"]', 'SecurePass123!');
    
    await page.click('[data-testid="submit"]');
    
    // Verify error message
    await expect(page.locator('[data-testid="error-message"]'))
      .toContainText('Email already exists');
  });

  test('form validation works correctly', async ({ page }) => {
    await page.goto('/register');
    
    // Submit empty form
    await page.click('[data-testid="submit"]');
    
    // Verify validation errors
    await expect(page.locator('[data-testid="email-error"]'))
      .toContainText('Email is required');
    await expect(page.locator('[data-testid="password-error"]'))
      .toContainText('Password is required');
  });
});
```

## Configuración

El comando utiliza `.claude/generate-tests-config.json`:

```json
{
  "defaultFramework": "jest",
  "defaultCoverage": 80,
  "testTypes": {
    "unit": {
      "enabled": true,
      "patterns": ["aaa", "bdd"],
      "mockStrategy": "auto",
      "edgeCases": "comprehensive"
    },
    "integration": {
      "enabled": true,
      "apiMocking": true,
      "databaseMocking": "in-memory",
      "cacheTests": true
    },
    "e2e": {
      "enabled": false,
      "framework": "playwright",
      "browsers": ["chromium", "firefox"],
      "devices": ["desktop", "mobile"]
    },
    "performance": {
      "enabled": false,
      "budgets": {
        "renderTime": "16ms",
        "bundleSize": "500KB",
        "memoryUsage": "50MB"
      }
    },
    "accessibility": {
      "enabled": true,
      "standards": ["wcag2.1", "section508"],
      "levels": ["AA"]
    }
  },
  "frameworks": {
    "jest": {
      "setupFiles": ["@testing-library/jest-dom"],
      "testEnvironment": "jsdom",
      "collectCoverageFrom": ["src/**/*.{js,jsx,ts,tsx}"]
    },
    "vitest": {
      "environment": "jsdom",
      "setupFiles": ["@testing-library/jest-dom"]
    },
    "cypress": {
      "baseUrl": "http://localhost:3000",
      "viewportWidth": 1280,
      "viewportHeight": 720
    },
    "playwright": {
      "baseURL": "http://localhost:3000",
      "use": {
        "screenshot": "only-on-failure",
        "video": "retain-on-failure"
      }
    }
  },
  "mocking": {
    "apiRequests": {
      "strategy": "msw",
      "generateMockData": true,
      "realisticData": true
    },
    "modules": {
      "strategy": "auto",
      "preserveImplementation": false
    },
    "dependencies": {
      "external": "mock",
      "internal": "spy"
    }
  },
  "codeAnalysis": {
    "detectTestableUnits": true,
    "identifyEdgeCases": true,
    "analyzeDependencies": true,
    "extractBusinessLogic": true
  }
}
```

## Salida del Comando

### Análisis Pre-generación
```
🧪 CLAUDE POWER - TEST GENERATION ANALYSIS
==========================================

📁 CÓDIGO ANALIZADO:
src/components/UserProfile.tsx (127 líneas)
  • 3 props analizadas (user, onEdit, className)
  • 5 estados internos detectados
  • 8 méall identificados
  • 12 casos edge identificados

📊 PLAN DE TESTS:
┌─────────────────┬─────────┬─────────────┬─────────────┐
│ Tipo Test       │ Cantidad│ Cobertura   │ Tiempo Est. │
├─────────────────┼─────────┼─────────────┼─────────────┤
│ Unit Tests      │   24    │    95%      │   8 min     │
│ Integration     │    6    │    85%      │   4 min     │
│ E2E Tests       │    3    │    70%      │  12 min     │
│ A11y Tests      │    8    │    90%      │   3 min     │
└─────────────────┴─────────┴─────────────┴─────────────┘

🎯 CASOS DETECTADOS:
✅ Rendering con props válidas
✅ Manejo de props faltantes/nulas
✅ Eventos de interacción
✅ Estados de loading/error
✅ Casos edge (nombres largos, caracteres especiales)
✅ Accessibility compliance
✅ Performance budgets
✅ Mobile responsiveness
```

### Tests Generados
```
📝 TESTS GENERADOS EXITOSAMENTE:
===============================

📁 files creados:
• src/components/__tests__/UserProfile.test.tsx (312 líneas)
• src/components/__tests__/UserProfile.integration.test.tsx (156 líneas)
• e2e/user-profile.spec.ts (89 líneas)
• src/components/__tests__/UserProfile.a11y.test.tsx (67 líneas)

📊 COBERTURA PROYECTADA:
• Statements: 96.8%
• Branches: 94.2%
• Functions: 100%
• Lines: 95.9%

🧪 RESUMEN DE TESTS:
• Total tests: 41
• Unit tests: 24 (✅ Rendering, interactions, edge cases)
• Integration tests: 6 (✅ API calls, state management)
• E2E tests: 3 (✅ User flows completos)
• Accessibility tests: 8 (✅ WCAG 2.1 compliance)

⚡ PERFORMANCE:
• Tiempo de ejecución estimado: 12.4s
• Memory usage: 85MB
• CPU usage: Medium

🎯 CALIDAD:
• Best practices: ✅ Implementadas
• Mocking strategy: ✅ Optimizada
• Test maintainability: ✅ Alta
• Edge cases coverage: ✅ Comprehensive
```

## Integración Avanzada

### CI/CD Pipeline
```yaml
name: Generated Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-generated:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Generate missing tests
        run: |
          npx claude-power generate-tests \
            --type=unit,integration \
            --coverage=90% \
            --auto-update
            
      - name: Run generated tests
        run: npm test -- --coverage --passWithNoTests
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          
      - name: Comment PR with coverage
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const coverage = JSON.parse(fs.readFileSync('./coverage/coverage-summary.json'));
            const comment = `
            ## 🧪 Test Coverage Report
            
            | Metric | Percentage | Status |
            |--------|------------|--------|
            | Statements | ${coverage.total.statements.pct}% | ${coverage.total.statements.pct >= 90 ? '✅' : '⚠️'} |
            | Branches | ${coverage.total.branches.pct}% | ${coverage.total.branches.pct >= 90 ? '✅' : '⚠️'} |
            | Functions | ${coverage.total.functions.pct}% | ${coverage.total.functions.pct >= 90 ? '✅' : '⚠️'} |
            | Lines | ${coverage.total.lines.pct}% | ${coverage.total.lines.pct >= 90 ? '✅' : '⚠️'} |
            
            Generated by Claude Power Test Generator 🤖
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
  "commands": [
    {
      "command": "claude-power.generateTests",
      "title": "Generate Tests",
      "category": "Claude Power"
    }
  ],
  "keybindings": [
    {
      "command": "claude-power.generateTests",
      "key": "ctrl+shift+t",
      "when": "editorTextFocus"
    }
  ],
  "tasks": [
    {
      "label": "Generate Tests for Current File",
      "type": "shell",
      "command": "npx",
      "args": [
        "claude-power",
        "generate-tests",
        "${file}",
        "--coverage=90%"
      ]
    }
  ]
}
```

---

*Parte del ecosistema **Claude Power** - Tests perfectos sin esfuerzo* 🧪🚀 
