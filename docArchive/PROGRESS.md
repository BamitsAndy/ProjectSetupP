# Development Progress

## Phase 1: Foundation

- [x] Project structure setup
- [x] proj-setup module
- [x] git-setup module
- [x] venv-setup module
- [x] cli-config module
- [x] project-init orchestrator
- [ ] Testing

## Developer Notes

### git-setup Module

**Location:** `src/project_setup/git_setup.py`

**Key Implementation Details:**
- Function `git_setup()` contains all logic (imported and wrapped in `proj_setup.py`)
- Uses `typer.Option(None, ...)` pattern for optional flags to support both interactive and non-interactive modes
- `is_interactive` flag determines whether to prompt or use defaults
- Uses `subprocess.run()` for git commands with `capture_output=True` and `check=True`
- Gitignore templates stored in `GITIGNORE_TEMPLATES` dict (Python, Node, Rust, Go, Blank)

**Non-interactive mode:** All required options must be provided via CLI flags
**Interactive mode:** Prompts for missing required options with sensible defaults

**Test command:**
```bash
python -m project_setup cli-config test-project --workflow assisted --cli both --server server --include-handoff
```

### project-init Module

**Location:** `src/project_setup/project_init.py`

**Key Implementation Details:**
- Main orchestrator that chains all other modules together
- Uses subprocess to call git-setup, venv-setup, and cli-config
- Creates IDE configuration files (.vscode/settings.json, .editorconfig)
- Sets up pytest testing structure if requested
- Performs git add and commit if git is enabled
- Supports both interactive and non-interactive modes

**CLI Options:**
- `--git`: Git mode: new, existing, or none
- `--name`: Project name
- `--url`: Repository URL for existing mode
- `--public`/`--private`: Repository visibility
- `--venv`/`--no-venv`: Create or skip virtual environment
- `--cli`: CLI tool: opencode, claude, or both
- `--server`: Server mode for opencode: local or server
- `--workflow`: Workflow type: agentic or assisted
- `--pytest`/`--no-pytest`: Set up or skip pytest testing

**Test command:**
```bash
python -m project_setup project-init --git new --name testproj --private --venv --cli opencode --server local --workflow agentic --pytest
```

### venv-setup Module

**Location:** `src/project_setup/venv_setup.py`

**Key Implementation Details:**
- Function `venv_setup()` contains all logic (imported and wrapped in `proj_setup.py`)
- Uses same `typer.Option(None, ...)` pattern as git-setup for optional flags
- `is_interactive` flag determines whether to prompt or use defaults
- Checks for `uv` first (preferred), falls back to `python -m venv`
- Uses `sys.platform` to determine activation command (Windows vs Unix)
- `update_gitignore()` adds `.venv/` to existing .gitignore or creates one
- Handles existing `.venv` directory (prompts to recreate unless `--yes` is used)
- Uses `subprocess.run()` with `capture_output=True` and `check=True` for venv creation

**CLI Options:**
- `project_dir`: Project directory path (prompts if not provided)
- `--yes`: Skip all prompts, create venv automatically
- `--use-uv`: Force use of uv for venv creation
- `--use-python`: Force use of python -m venv

**Test command:**
```bash
python -m project_setup venv-setup test-project --yes
```

**Activation:** Output shows platform-specific activation command:
- Windows: `path\to\project\.venv\Scripts\activate.bat`
- Unix: `source path/to/project/.venv/bin/activate`

### cli-config Module

**Location:** `src/project_setup/cli_config.py`

**Key Implementation Details:**
- Function `cli_config()` contains all logic (imported and wrapped in `proj_setup.py`)
- Uses same `typer.Option(None, ...)` pattern as other modules for optional flags
- `is_interactive` flag determines whether to prompt or use defaults
- Creates `.opencode/settings.json` for opencode with server and workflow
- Creates `.claude/settings.json` for claude with workflow
- Supports `--include-handoff` to create handoff plugin placeholder
- Creates `.opencode/commands/init.py` if requested in interactive mode

**CLI Options:**
- `project_dir`: Project directory path (prompts if not provided)
- `--workflow`: Workflow type: agentic or assisted
- `--cli`: CLI tool: opencode, claude, or both
- `--server`: Server mode for opencode: local or server
- `--include-handoff`: Include handoff plugin (for both mode)

**Test commands:**
```bash
python -m project_setup cli-config test-project --workflow agentic --cli opencode --server local
python -m project_setup cli-config test-project --workflow assisted --cli both --server server --include-handoff
```
