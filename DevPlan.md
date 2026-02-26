# Development Plan - Project Setup Tool

## Overview
A modular CLI tool for setting up new coding projects with git, venv, and CLI tool configuration support.

---

## Architecture

### Discrete Tools
| Tool | Purpose |
|------|---------|
| `proj-setup` | Project scaffolding (folder, basic files) |
| `git-setup` | Git initialization/clone + remote creation |
| `venv-setup` | Virtual environment management |
| `cli-config` | CLI tool configuration (opencode, claude) |
| `project-init` | Orchestrator - main entry point |

### File Structure
```
project-setup/
├── pyproject.toml
├── src/
│   └── project_setup/
│       ├── __init__.py
│       ├── cli.py
│       ├── git_setup.py
│       ├── proj_setup.py
│       ├── venv_setup.py
│       ├── cli_config.py
│       └── project_init.py
├── tests/
└── README.md
```

---

## Functional Specification

### 1. Git Setup (`git-setup`)
- **Modes:** `new` | `existing` | `none`
- **New mode:** Create repo, .gitignore (templates: Python, Node, Rust, Go, Blank), README.md
- **Existing mode:** Clone from URL
- **None mode:** Skip git entirely

### 2. Venv Setup (`venv-setup`)
- Uses `uv venv` (preferred) or `python -m venv`
- Adds `.venv/` to `.gitignore`
- Platform-specific activation commands

### 3. CLI Configuration (`cli-config`)
- Workflow: `agentic` | `assisted`
- CLI tools: `opencode`, `claude`, or `both`
- Server mode: `local` | `server`
- Optional handoff plugin configuration

### 4. IDE Configuration
- `.vscode/settings.json` and `extensions.json`
- `.editorconfig`

### 5. Testing Setup
- Prompt for `pytest` | `none`
- Creates `tests/` structure if pytest selected

---

## Testing Plan

### Prerequisites
- pytest installed: `pip install pytest`
- Run from project root: `python -m pytest tests/`

### Test Structure
- **Unit Tests:** `tests/test_git_setup.py`, `tests/test_venv_setup.py`, `tests/test_cli_config.py`, `tests/test_orchestrator.py`
- **E2E Tests:** Full workflow tests via CLI commands

---

## Release Checklists

### UAT Release (v0.1)
- [x] Project structure setup
- [x] proj-setup module
- [x] git-setup module
- [x] venv-setup module
- [x] cli-config module
- [x] project-init orchestrator
- [x] Unit tests (15 tests passed)
- [x] E2E tests (all passed)

### Pre-Release Tasks
- [ ] **Code Review:** Review all source files for quality, error handling, and edge cases
- [ ] **Code Cleanup:** Remove debug statements, optimize imports, ensure consistent formatting
- [ ] **README.md:** Update with installation, usage examples, and contribution guidelines

---

## Future Roadmap

### Phase 2: Language Expansion (v0.2)
- [ ] JavaScript/TypeScript support (npm/yarn/pnpm)
- [ ] Rust support (Cargo)
- [ ] Go support

### Phase 3: Package Managers (v0.3)
- [ ] Poetry support
- [ ] Pipenv support

### Phase 4: Remote Integration (v0.4)
- [ ] GitHub API integration - create remote repo
- [ ] GitLab API integration
- [ ] Auto-push after setup

### Phase 5-9: Additional Features
- Project structure templates (Library, CLI, Web API, Web App)
- CI/CD templates (GitHub Actions, GitLab CI)
- Docker support
- License selection
- Installation via pip

---

## Interface Between Tools

Each tool is a separate CLI script. Communication via:
- **Subprocess calls** - Each tool invoked as separate process
- **Arguments** - Data passed via CLI flags/arguments
- **Exit codes** - Success (0) or failure (non-zero)
- **stdout** - Output project directory path for chaining

---

## Acceptance Criteria

1. Tool runs interactively with clear prompts
2. Tool accepts flags for automated runs
3. Git new: creates folder, .gitignore, README.md
4. Git existing: clones repo to specified folder
5. Venv: creates .venv, adds to .gitignore
6. CLI config: creates appropriate config files
7. All operations are idempotent where possible
8. Clear error messages on failure
9. Works on Windows, macOS, Linux
