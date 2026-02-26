# Project Setup Tool

A modular CLI tool for setting up new coding projects with Git, virtual environments, CLI configurations, IDE settings, and testing infrastructure.

## Installation

```bash
pip install project-setup
```

Or install from source:

```bash
cd ProjectSetup
pip install -e .
```

## Usage

### project-init (Main Orchestrator)

The main command that chains all modules together for complete project setup.

**Interactive mode:**
```bash
project-init
```

**Non-interactive mode:**
```bash
project-init --git new --name my-project --private --venv --cli opencode --server local --workflow agentic --pytest
```

### git-setup

Initialize Git repositories or clone existing ones.

```bash
# Create new repository (interactive)
git-setup

# Create new repository with options
git-setup my-project --mode new --template Python --include-gitignore --include-readme

# Clone existing repository
git-setup --mode existing --url https://github.com/user/repo.git

# Local directory only (no git)
git-setup my-project --mode none
```

### venv-setup

Create Python virtual environments.

```bash
# Interactive mode
venv-setup

# Non-interactive (auto-confirm)
venv-setup my-project --yes

# Force using uv or python
venv-setup my-project --use-uv
venv-setup my-project --use-python
```

### cli-config

Configure CLI tool settings (opencode, Claude, or both).

```bash
# Interactive mode
cli-config my-project

# With options
cli-config my-project --workflow agentic --cli both --server local --include-handoff
```

## Features

### Git Modes
- **new**: Initialize a new local Git repository
- **existing**: Clone an existing repository
- **none**: Create project directory without Git

### .gitignore Templates
- Python
- Node
- Rust
- Go
- Blank

### Virtual Environment
- **uv**: Fast Python package installer (preferred)
- **python -m venv**: Standard Python venv

### CLI Configuration
- **opencode**: Configures `.opencode/settings.json`
- **claude**: Configures `.claude/settings.json`
- **both**: Configures both
- Server modes: `local` or `server`
- Workflow types: `agentic` or `assisted`

### IDE Configuration
- **.vscode/settings.json**: Python interpreter, formatting, import organization
- **.editorconfig**: Cross-editor code style settings

### Testing
- **pytest** setup with `tests/` directory and `pytest.ini`

## Examples

### Full Project Setup (Interactive)
```bash
$ project-init
=== Project Initialization ===

Git mode (new/existing/none) [new]: new
Project name: my-awesome-project
Visibility (public/private) [private]: private
Description (optional) []: A new project
Include .gitignore? [Y/n]: Y
Gitignore template (Python/Node/Rust/Go/Blank) [Python]: Python
Include README? [Y/n]: Y
Create virtual environment? [Y/n]: Y
Primary CLI tool (opencode/claude/both) [both]: both
Workflow type (agentic/assisted) [assisted]: agentic
Opencode server mode (local/server) [local]: local
Include handoff plugin? (y/n) [n]: n
Set up pytest testing? [Y/n]: Y
```

### Minimal Setup (Non-interactive)
```bash
project-init --git new --name my-project --no-venv --no-pytest
```

### Clone and Configure
```bash
git-setup --mode existing --url https://github.com/user/repo.git
venv-setup repo --yes
cli-config repo --cli opencode --server local
```

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Commit your changes
6. Push to the branch
7. Create a Pull Request

## License

MIT License
