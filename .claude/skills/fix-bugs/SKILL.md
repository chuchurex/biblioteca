---
name: fix-bugs
description: "Automatic bug detection and fixing using advanced AI"
---

# Fix Bugs Command

Auto-detects, analyzes, and fixes bugs automatically using advanced AI, reducing production bugs by up to 90%.

## Description

The `/fix-bugs` command represents the future of bug fixing:

- **Automatic detection** of common and complex bugs
- **Root cause analysis** to understand the real problem
- **Intelligent correction** that preserves functionality
- **Automatic testing** of fixes before applying
- **Learning mode** that learns from project patterns
- **Safe mode** with automatic rollback if something goes wrong
- **Detailed explanations** of each applied fix
- **Prevention suggestions** to avoid similar bugs

## Usage

```
/fix-bugs [directory] [--types] [--confidence] [--mode] [--test-after]
```

### Parameters

- `directory`: specific directory to analyze and fix
- `--types`: Types of bugs to look for (memory-leaks, null-pointers, race-conditions, etc.)
- `--confidence`: Minimum confidence level to apply fixes (low, medium, high)
- `--mode`: Operation mode (safe, aggressive, learning, preview)
- `--test-after`: Run tests after each fix
- `--rollback-on-fail`: Automatic rollback if tests fail
- `--explain`: Explain each fix made
- `--prevent`: Suggest changes to prevent similar bugs

### Examples

```
/fix-bugs
/fix-bugs src/ --types=memory-leaks,null-pointers --confidence=high
/fix-bugs --mode=safe --test-after --rollback-on-fail
/fix-bugs utils/ --mode=learning --explain
/fix-bugs --types=race-conditions --confidence=medium --prevent
/fix-bugs components/ --mode=preview --dry-run
```

## Types of Bugs Detected and Fixed

### 🚨 Memory Leaks
```javascript
// ❌ BEFORE - Memory leak detected
function DataProcessor() {
  const data = [];
  
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData().then(newData => {
        data.push(...newData); // Memory leak: array grows indefinitely
      });
    }, 1000);
    
    // Missing cleanup
  }, []);
  
  return <div>{data.length} items</div>;
}

// ✅ AFTER - Automatic fix applied
function DataProcessor() {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const interval = setInterval(() => {
      fetchData().then(newData => {
        setData(prevData => {
          // Limit array size to prevent memory leak
          const combined = [...prevData, ...newData];
          return combined.slice(-1000); // Keep only last 1000 items
        });
      });
    }, 1000);
    
    // Automatically added cleanup
    return () => clearInterval(interval);
  }, []);
  
  return <div>{data.length} items</div>;
}
```

### 🎯 Null Pointer Exceptions
```javascript
// ❌ BEFORE - Potential null pointer
function UserProfile({ user }) {
  return (
    <div>
      <h1>{user.name}</h1> {/* Crash if user is null */}
      <img src={user.avatar.url} alt="Avatar" /> {/* Double null risk */}
      <p>Joined: {user.createdAt.toLocaleDateString()}</p>
    </div>
  );
}

// ✅ AFTER - Null safety automatically added
function UserProfile({ user }) {
  // Null check automatically added
  if (!user) {
    return <div>Loading user...</div>;
  }
  
  return (
    <div>
      <h1>{user.name || 'Anonymous User'}</h1>
      <img 
        src={user.avatar?.url || '/default-avatar.png'} 
        alt="Avatar" 
        onError={(e) => { e.target.src = '/default-avatar.png'; }}
      />
      <p>
        Joined: {user.createdAt ? 
          new Date(user.createdAt).toLocaleDateString() : 
          'Unknown'
        }
      </p>
    </div>
  );
}
```

### ⚡ Race Conditions
```javascript
// ❌ BEFORE - Race condition in async operations
async function updateUserData(userId, newData) {
  const user = await fetchUser(userId);
  const updated = { ...user, ...newData };
  
  // Race condition: user might have changed between fetch and save
  await saveUser(userId, updated);
}

// ✅ AFTER - Race condition eliminated
async function updateUserData(userId, newData) {
  let retries = 3;
  
  while (retries > 0) {
    try {
      const user = await fetchUser(userId);
      const updated = { ...user, ...newData, version: user.version + 1 };
      
      // Optimistic locking automatically added
      await saveUserWithVersion(userId, updated, user.version);
      return updated;
    } catch (error) {
      if (error.code === 'VERSION_CONFLICT' && retries > 1) {
        retries--;
        // Exponential backoff added
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, 3 - retries) * 100));
        continue;
      }
      throw error;
    }
  }
}
```

### 🔄 Infinite Loops / Recursion
```javascript
// ❌ BEFORE - Potential infinite recursion
function calculateFactorial(n) {
  if (n === 0) return 1;
  return n * calculateFactorial(n - 1); // No protection against negative numbers
}

// ✅ AFTER - Safe recursion with guards
function calculateFactorial(n) {
  // Input validation automatically added
  if (typeof n !== 'number' || !Number.isInteger(n)) {
    throw new Error('Input must be a non-negative integer');
  }
  
  if (n < 0) {
    throw new Error('Factorial is not defined for negative numbers');
  }
  
  // Stack overflow protection
  if (n > 170) {
    throw new Error('Number too large: factorial would exceed JavaScript number limits');
  }
  
  if (n === 0 || n === 1) return 1;
  return n * calculateFactorial(n - 1);
}
```

### 🌐 Async/Await Issues
```javascript
// ❌ BEFORE - Unhandled promise rejections
async function processData() {
  const data = await fetchData(); // Unhandled if it throws
  data.forEach(async item => {
    await processItem(item); // Won't wait for completion
  });
  
  console.log('All done!'); // Executes immediately
}

// ✅ AFTER - Proper async handling
async function processData() {
  try {
    const data = await fetchData();
    
    // Promise.all added for concurrent processing
    await Promise.all(
      data.map(async item => {
        try {
          return await processItem(item);
        } catch (error) {
          console.error(`Failed to process item ${item.id}:`, error);
          // Continue processing other items
          return null;
        }
      })
    );
    
    console.log('All processing completed!');
  } catch (error) {
    console.error('Failed to fetch data:', error);
    throw new Error(`Data processing failed: ${error.message}`);
  }
}
```

### 🔐 Security Vulnerabilities
```javascript
// ❌ BEFORE - XSS vulnerability
function UserComment({ comment }) {
  return (
    <div 
      dangerouslySetInnerHTML={{ __html: comment.text }} // XSS risk
    />
  );
}

// ✅ AFTER - XSS protection added
import DOMPurify from 'dompurify';

function UserComment({ comment }) {
  // Automatic sanitization added
  const sanitizedText = DOMPurify.sanitize(comment.text, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href'],
    ALLOWED_URI_REGEXP: /^https?:\/\//
  });
  
  return (
    <div 
      dangerouslySetInnerHTML={{ __html: sanitizedText }}
    />
  );
}
```

## Configuration

`.claude/fix-bugs-config.json`:

```json
{
  "confidence": {
    "minimum": "medium",
    "autoApply": "high",
    "requireConfirmation": "low"
  },
  "bugTypes": {
    "memoryLeaks": {
      "enabled": true,
      "priority": "high",
      "patterns": ["event-listeners", "intervals", "observers", "subscriptions"]
    },
    "nullPointers": {
      "enabled": true,
      "priority": "high",
      "addGuards": true,
      "defaultValues": true
    },
    "raceConditions": {
      "enabled": true,
      "priority": "medium",
      "addLocking": true,
      "retryLogic": true
    },
    "infiniteLoops": {
      "enabled": true,
      "priority": "high",
      "maxIterations": 10000,
      "stackProtection": true
    },
    "asyncIssues": {
      "enabled": true,
      "priority": "medium",
      "promiseHandling": true,
      "errorBoundaries": true
    },
    "securityVulns": {
      "enabled": true,
      "priority": "critical",
      "autoSanitize": true,
      "validateInputs": true
    },
    "performanceIssues": {
      "enabled": false,
      "priority": "low",
      "inefficientAlgorithms": true,
      "memoryOptimization": true
    }
  },
  "safety": {
    "backupBeforeFix": true,
    "runTestsAfterFix": true,
    "rollbackOnTestFail": true,
    "maxFilesPerRun": 10,
    "requireUserConfirmation": false
  },
  "learning": {
    "enabled": true,
    "storePatterns": true,
    "adaptToProject": true,
    "suggestPreventions": true
  },
  "testing": {
    "generateTestsForFixes": true,
    "runExistingTests": true,
    "performanceRegression": true,
    "securityRegression": true
  }
}
```

## Command Output

### Bug Analysis
```
🔧 CLAUDE POWER - BUG DETECTION & FIXING
========================================

🔍 ANALYSIS COMPLETED:
scanned files: 127
analyzed lines: 15,847
analysis time: 23.4s

🚨 DETECTED BUGS:
┌─────────────────────┬─────────┬─────────────┬─────────────┐
│ Type                │ Count   │ Severity    │ Fixable     │
├─────────────────────┼─────────┼─────────────┼─────────────┤
│ Memory Leaks        │    8    │ High        │     8       │
│ Null Pointers       │   15    │ High        │    15       │
│ Race Conditions     │    3    │ Medium      │     3       │
│ Infinite Loops      │    2    │ High        │     2       │
│ Async Issues        │   12    │ Medium      │    11       │
│ Security Vulns      │    4    │ Critical    │     4       │
│ Performance Issues  │    7    │ Low         │     5       │
└─────────────────────┴─────────┴─────────────┴─────────────┘

🎯 CONFIDENCE LEVELS:
• High Confidence: 32 bugs (auto-fix available)
• Medium Confidence: 15 bugs (review recommended)
• Low Confidence: 3 bugs (manual review required)

⚡ TOTAL IMPACT:
• Critical bugs that could crash app: 19
• Security vulnerabilities: 4
• Performance degradations: 7
• Maintainability issues: 20
```

### Applied Fixes
```
🔧 AUTOMATICALLY APPLIED FIXES:
==================================

📁 src/components/UserDashboard.tsx
  🚨 [CRITICAL] Memory leak in useEffect (line 45)
    ✅ Fixed: Added cleanup in return statement
    ✅ Tested: Unit tests passing
    💡 Prevention: Use custom hook useInterval for intervals

📁 src/utils/dataProcessor.js  
  🎯 [HIGH] Null pointer in processUserData (line 78)
    ✅ Fixed: Added null guards and default values
    ✅ Tested: Integration tests passing
    💡 Prevention: Use TypeScript for null safety

📁 src/services/ApiService.js
  ⚡ [MEDIUM] Race condition in updateUser (line 134)
    ✅ Fixed: Implemented optimistic locking
    ✅ Tested: Race condition tests added
    💡 Prevention: Implement state management with Redux Toolkit

📁 src/hooks/useAuth.ts
  🔐 [CRITICAL] XSS vulnerability in user input (line 23)
    ✅ Fixed: Added sanitization with DOMPurify
    ✅ Tested: Security tests added
    💡 Prevention: Input validation in backend as well

🧪 TESTING RESULTS:
• Tests executed: 247
• Tests passing: 247 (100%)
• New coverage: 94.2% (+3.1%)
• Execution time: 12.3s
• Performance regression: None detected

📊 POST-FIX METRICS:
• Critical bugs eliminated: 19 → 0 (100% reduction)
• Security vulnerabilities: 4 → 0 (100% reduction)
• Static warnings: 87 → 23 (73% reduction)
• Average cyclomatic complexity: 8.2 → 6.4 (22% improvement)

💡 SUGGESTED PREVENTION:
1. Configure ESLint rules for memory leaks
2. Implement TypeScript strict mode
3. Add pre-commit hooks for security scanning
4. Setup automated dependency vulnerability scanning
5. Implement error boundaries in React components
```

### Learning Mode Output
```
🧠 CLAUDE POWER - LEARNING MODE INSIGHTS
========================================

📈 DETECTED PATTERNS IN YOUR PROJECT:
• Frequent use of useEffect without cleanup (8 cases)
• Common pattern: fetching data in components (12 cases)
• Anti-pattern: inconsistent null checks (15 cases)
• Memory leak pattern: intervals without clear (5 cases)

🎯 PERSONALIZED RECOMMENDATIONS:
1. Create custom hook useApiData for data fetching
2. Implement utility function saflyAccess for null safety
3. Setup ESLint rule react-hooks/exhaustive-deps
4. Create wrapper component for error boundaries

📚 UPDATED KNOWLEDGE BASE:
• Saved 23 new project-specific bug patterns
• Updated confidence in 12 types of fixes
• Learned 8 new prevention strategies
• Generated 15 custom ESLint rules

🔄 AUTOMATIC ADAPTATION:
• Confidence levels adjusted based on success rate
• Fix templates updated for your coding style
• Automatic exclusions for detected false positives
• Priorities rebalanced according to impact on your codebase
```

## Advanced Integrations

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔧 Running auto bug detection and fixing..."

# Run bug detection with high confidence auto-fix
npx claude-power fix-bugs \
  --staged-only \
  --confidence=high \
  --test-after \
  --rollback-on-fail

if [ $? -ne 0 ]; then
  echo "❌ Critical bugs detected that require manual review"
  echo "Run 'npx claude-power fix-bugs --mode=preview' to see issues"
  exit 1
fi

echo "✅ No critical bugs detected, commit proceeding"
```

### GitHub Actions
```yaml
name: Auto Bug Fix

on:
  push:
    branches: [develop, feature/*]
  pull_request:
    branches: [main, develop]

jobs:
  auto-fix-bugs:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Setup Node.js
        uses: actions/setup-node@v3
        
      - name: Install dependencies
        run: npm ci
        
      - name: Run auto bug fixes
        run: |
          npx claude-power fix-bugs \
            --confidence=high \
            --test-after \
            --mode=safe \
            --output=json > bug-fixes.json
            
      - name: Commit auto-fixes
        run: |
          if [ -s bug-fixes.json ]; then
            git config --local user.email "action@github.com"
            git config --local user.name "Claude Power Auto-Fix"
            git add .
            git commit -m "fix: auto-fix bugs detected by Claude Power
            
            $(cat bug-fixes.json | jq -r '.fixes[].description' | head -5)
            
            Co-authored-by: Claude Power <claude@anthropic.com>"
            git push
          fi
```

---

*Part of the **Claude Power** ecosystem - Bugs automatically eliminated* 🔧🚀 
