# Project Setup Tool - PLAN

## Overview
A modular CLI tool for setting up new coding projects with git, venv, and CLI tool configuration support.

## Architecture

### Discrete Tools
| Tool | Purpose |
|------|---------|
| `proj-setup` | Project scaffolding (folder, basic files) |
| `git-setup` | Git initialization/clone + remote creation |
| `venv-setup` | Virtual environment management |
| `cli-config` | CLI tool configuration (opencode, claude) |
| `project-init` | Orchestrator - main entry point |

## Functional Specification

### 1. Git Setup (`git-setup`)

**Inputs:**
- Mode: `new` | `existing` | `none`
- If `new`:
  - Repository name
  - Visibility: `public` | `private`
  - Description (optional)
  - Initialize with `.gitignore` (template selection)
  - Initialize with `README.md`
  - Create remote on GitHub (optional, future: ROADMAP)
- If `existing`:
  - Repository URL (SSH or HTTPS)
  - Clone to local folder (prompt for folder name)
- If `none`: Skip git entirely, proceed to project name prompt

**Outputs:**
- Initialized git repo OR cloned repo in target directory
- `.gitignore` with appropriate template
- `README.md` with project name and description

### 2. Project Setup (`proj-setup`)

**Inputs:**
- Project name (if not provided by git)
- Target directory

**Outputs:**
- Project folder created
- Basic structure: `src/` or flat depending on choice

### 3. Venv Setup (`venv-setup`)

**Inputs:**
- Create venv: `yes` | `no`
- If `yes`:
  - Use `uv venv` (preferred) or `python -m venv`

**Outputs:**
- `.venv/` created and activated (outputs activation command)
- `.venv/` added to `.gitignore`

### 4. CLI Configuration (`cli-config`)

**Inputs:**
- Workflow type: `agentic` | `assisted`
- Primary CLI: `opencode` | `claude` | `both`
- If `opencode`:
  - Server mode: `server` | `local`
- If `claude`:
  - Config options (future: read from existing claude settings)
- If `both`:
  - Include handoff plugin configuration
- Additional steps: `/init` for opencode, similar for others

**Outputs:**
- `.opencode/` configuration directory with settings
- `.claude/` configuration (as applicable)
- Project-specific config files

### 5. Project Init (Orchestrator)

**Flow:**
1. Git Setup → determines directory
2. cd into directory
3. Venv Setup
4. CLI Configuration
5. IDE Configuration (basic)
6. Testing framework prompt
7. Update git (if git enabled)

**CLI Interface:**
- Interactive mode: `project-init` (prompts for everything)
- Flag mode: `project-init --git new --name myproject --private --venv`

## IDE Configuration (Phase 1)

- `.vscode/` directory with:
  - `settings.json` (language-specific defaults)
  - `extensions.json` (recommended extensions)
- `.editorconfig` (basic editor settings)

## Testing Setup (Phase 1)

- Prompt for testing framework: `pytest` | `none`
- If `pytest`: create `tests/` structure, `pyproject.toml` or `pytest.ini`

## File Structure
```
project-setup/
├── pyproject.toml
├── src/
│   └── project_setup/
│       ├── __init__.py
│       ├── cli.py          # Click/Typer CLI
│       ├── git_setup.py
│       ├── proj_setup.py
│       ├── venv_setup.py
│       ├── cli_config.py
│       └── orchestrator.py
├── tests/
└── README.md
```

## Interface Between Tools

Each tool is a separate CLI script. Communication via:
- **Subprocess calls** - Each tool invoked as separate process
- **Arguments** - Data passed via CLI flags/arguments
- **Exit codes** - Success (0) or failure (non-zero)
- **stdout** - Output project directory path for chaining

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
