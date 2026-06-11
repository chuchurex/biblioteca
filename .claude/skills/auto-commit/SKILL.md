---
name: auto-commit
description: "Generates automatic commits with intelligent descriptions based on detected changes"
---

# Auto Commit Command

Generates automatic commits with intelligent descriptions based on detected changes in the project.

## Description

The `/auto-commit` command analyzes pending changes in the Git repository and automatically generates:

- **Descriptive commit messages** following standard conventions
- **Impact analysis** of changes made
- **Automatic categorization** of change type (feat, fix, docs, etc.)
- **Detection of breaking changes** and important changes
- **Validation** before commit to prevent errors
- **Improvement suggestions** in the generated message

## Usage

```
/auto-commit [--type] [--scope] [--message] [--validate] [--format]
```

### Parameters

- `--type`: Force a specific type (feat, fix, docs, style, refactor, test, chore)
- `--scope`: Specify the scope of the change (component, module, etc.)
- `--message`: Add additional custom message
- `--validate`: Run validations before commit (lint, tests, build)
- `--format`: Commit format (conventional, angular, simple)
- `--interactive`: Interactive mode to review before committing
- `--dry-run`: Show the generated message without committing

### Examples

```
/auto-commit
/auto-commit --type=feat --scope=authentication
/auto-commit --message="implement social login" --validate=true
/auto-commit --format=conventional --interactive
/auto-commit --dry-run
/auto-commit --type=fix --validate=lint,test
```

## Automatic Change Analysis

### Change Type Detection

#### 🚀 feat (New features)
- New files added
- New functions or methods
- New React components
- New routes or endpoints
- New main dependencies

#### 🐛 fix (Bug fixes)
- Changes in conditionals or logic
- Typo corrections
- Improved error handling
- CSS or style fixes
- Import corrections

#### 📚 docs (Documentation)
- Changes in .md files
- Comment updates
- README modified
- JSDoc changes

#### 💄 style (Formatting/style)
- Format-only changes
- Linting adjustments
- Whitespace
- Import organization

#### ♻️ refactor (Refactoring)
- Code reorganization
- Function extraction
- Name changes
- Optimizations without functional change

#### ✅ test (Tests)
- .test.* or .spec.* files
- __tests__ folders
- Testing configuration

#### 🔧 chore (Maintenance tasks)
- package.json modified
- Build configuration
- Automation scripts
- .gitignore updated

### Scope Detection

```javascript
// Automatically detects scope based on:
src/components/auth/ → scope: "auth"
src/pages/dashboard/ → scope: "dashboard"  
backend/api/users/ → scope: "users-api"
styles/theme/ → scope: "theme"
docs/setup/ → scope: "docs"
```

### Impact Analysis

- **Breaking Changes**: Changes in public APIs, function removal
- **Major**: Important new features, large refactors
- **Minor**: Minor new features, improvements
- **Patch**: Bug fixes, documentation, style

## Configuration

The command uses `.claude/auto-commit-config.json`:

```json
{
  "format": "conventional",
  "validation": {
    "runLint": true,
    "runTests": false,
    "checkBuild": false,
    "maxFileChanges": 50
  },
  "templates": {
    "feat": "{type}({scope}): {description}\\n\\n{details}\\n\\n{footer}",
    "fix": "{type}({scope}): {description}\\n\\n{details}\\n\\n{footer}",
    "docs": "{type}({scope}): {description}",
    "style": "{type}: {description}",
    "refactor": "{type}({scope}): {description}\\n\\n{details}",
    "test": "{type}({scope}): {description}",
    "chore": "{type}: {description}"
  },
  "scopes": {
    "autoDetect": true,
    "predefined": [
      "auth",
      "api", 
      "ui",
      "components",
      "utils",
      "config",
      "docs",
      "tests"
    ]
  },
  "rules": {
    "maxSubjectLength": 100,
    "bodyWrap": 72,
    "requireBody": ["feat", "fix", "refactor"],
    "requireBreakingChange": true,
    "requireTicketNumber": false
  },
  "ai": {
    "useIntelligentDescriptions": true,
    "contextAnalysis": true,
    "suggestImprovements": true,
    "detectBreakingChanges": true
  }
}
```

## Command Output

### Change Analysis
```
🤖 CLAUDE POWER - AUTO COMMIT ANALYSIS
======================================

📊 DETECTED CHANGES:
┌─────────────────┬─────────┬─────────────┐
│ Type            │ files│ Lines       │
├─────────────────┼─────────┼─────────────┤
│ Modified        │    8    │ +156 -42    │
│ New             │    3    │ +203        │
│ Deleted         │    1    │ -67         │
│ Renamed         │    2    │ ~           │
└─────────────────┴─────────┴─────────────┘

🔍 INTELLIGENT ANALYSIS:
📁 src/components/auth/
  ✨ [FEAT] LoginForm.tsx - New login component
  ✨ [FEAT] AuthContext.tsx - Auth context
  
📁 src/pages/
  🐛 [FIX] dashboard.tsx - Fix navigation error
  
📁 docs/
  📚 [DOCS] README.md - Update installation guide

🎯 DETECTED TYPE: feat
🏷️ SUGGESTED SCOPE: auth
⚡ IMPACT: Minor (new functionality)
```

### Generated Message
```
💬 GENERATED COMMIT MESSAGE:
=====================================

feat(auth): implement authentication system with social login

- Add LoginForm component with validation
- Implement AuthContext for state management
- Fix navigation in dashboard after login
- Update setup documentation

Allows users to authenticate using:
- Traditional email/password  
- Login with Google OAuth
- Login with GitHub OAuth

Breaking changes: None
Closes: #123, #124
```

### Pre-commit Validations
```
🔍 PRE-COMMIT VALIDATIONS:
==========================

✅ ESLint: 0 errors, 2 warnings
✅ Prettier: Correct format
✅ TypeScript: Successful compilation
⚠️ Tests: 2 pending tests for new components
✅ Build: Successful generation
✅ File size: Within limits

🚦 RESULT: ✅ READY TO COMMIT
```

### Interactive Options
```
📝 PROCEED WITH COMMIT?

Proposed message:
> feat(auth): implement authentication system with social login

Options:
[Y] Yes, commit
[E] Edit message
[A] Add details
[C] Change type/scope  
[V] View full diff
[N] Cancel

Choice: 
```

## Advanced Integrations

### Webhooks and Notifications
```json
{
  "integrations": {
    "slack": {
      "enabled": true,
      "webhook": "https://hooks.slack.com/...",
      "channel": "#dev-commits"
    },
    "jira": {
      "enabled": true,
      "autoLink": true,
      "transitionTickets": false
    },
    "github": {
      "autoLabel": true,
      "linkIssues": true,
      "assignReviewers": true
    }
  }
}
```

### Custom Templates
```json
{
  "customTemplates": {
    "hotfix": "hotfix: {description}\\n\\nUrgent fix for: {issue}\\n\\nTested: {testDetails}",
    "release": "release: version {version}\\n\\n{changelogSummary}\\n\\nBreaking Changes:\\n{breakingChanges}",
    "security": "security: {description}\\n\\n⚠️ Security fix\\n\\nCVE: {cve}\\nSeverity: {severity}"
  }
}
```

## Special Use Cases

### Merge/Release Commits
```bash
# Auto-generate message for merge
/auto-commit --type=merge --message="feat/user-dashboard into main"

# Release commit with automatic changelog
/auto-commit --type=release --message="v2.1.0" --changelog=true

# Urgent hotfix
/auto-commit --type=hotfix --validate=minimal --priority=high
```

### Multiple Contexts
```bash
# Commit for specific feature
/auto-commit --scope=dashboard --context=feature/user-dashboard

# Cross-platform commit
/auto-commit --platform=web,mobile --sync=true

# Commit with dependencies
/auto-commit --dependencies=updated --security-check=true
```

### AI Contextual Analysis

```
🧠 AI CONTEXTUAL ANALYSIS:
=========================

📈 DETECTED PATTERNS:
• This commit continues the work on authentication started 3 commits ago
• Component-driven development pattern detected
• Code follows established project conventions

💡 SUGGESTIONS:
• Consider adding tests for LoginForm.tsx
• Change in AuthContext may affect other components
• Document new OAuth providers in wiki

🎯 COMMIT QUALITY:
• Message: 9/10 (clear and descriptive)
• Scope: 10/10 (well defined)
• Impact: 8/10 (important change well documented)
```

## Automation and CI/CD

### GitHub Actions
```yaml
name: Auto Commit Quality Check

on:
  push:
    branches: [feature/*, develop]

jobs:
  commit-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate commit message
        run: |
          COMMIT_MSG=$(git log -1 --pretty=%B)
          npx claude-power validate-commit "$COMMIT_MSG"
          
      - name: Analyze commit quality
        run: |
          npx claude-power analyze-commit --output=json > commit-analysis.json
          
      - name: Comment on PR if quality issues
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const analysis = JSON.parse(fs.readFileSync('commit-analysis.json'));
            if (analysis.score < 8) {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: `## 📝 Commit Quality Analysis\n\nScore: ${analysis.score}/10\n\n${analysis.suggestions.join('\n')}`
              });
            }
```

### Pre-commit Hook Integration
```bash
#!/bin/sh
# .git/hooks/prepare-commit-msg

# If no message or very basic, generate an automatic one
if [ -z "$2" ] || [ "$2" = "message" ]; then
  echo "🤖 Generating intelligent commit message..."
  AUTO_MSG=$(npx claude-power auto-commit --dry-run --format=conventional)
  echo "$AUTO_MSG" > "$1"
  echo "✅ Message generated. Edit if necessary."
fi
```

---

*Part of the **Claude Power** ecosystem - Automate your workflow with AI* 🚀 
