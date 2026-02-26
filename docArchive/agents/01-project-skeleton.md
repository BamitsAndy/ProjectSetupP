# Agent 1: Project Skeleton

## Task
Create the directory structure and base files for the project-setup tool.

## Working Directory
`D:\python\GIT\ProjectSetup`

## Deliverables

### 1. Directory Structure
Create the following directories:
```
project-setup/
├── src/
│   └── project_setup/
├── tests/
```

### 2. pyproject.toml
Create `pyproject.toml` in the root with:
- Package name: `project-setup`
- Python version: `>=3.10`
- Dependencies: `typer`, `click` (for CLI)
- Build system: `hatchling` or `setuptools`
- Entry points: define CLI commands for `proj-setup`, `git-setup`, `venv-setup`, `cli-config`, `project-init`

### 3. Empty Module Files
Create these empty files with basic docstrings:
- `src/project_setup/__init__.py`
- `src/project_setup/__main__.py`
- `src/project_setup/proj_setup.py`
- `src/project_setup/git_setup.py`
- `src/project_setup/venv_setup.py`
- `src/project_setup/cli_config.py`
- `src/project_setup/project_init.py`

### 4. Test Directory
Create:
- `tests/__init__.py`

## Verification
- Run `python -c "import project_setup"` to verify package imports
- Verify directory structure with `ls -R`

## Notes
- Keep all files minimal/empty - just imports and docstrings
- Do NOT implement any functionality yet
- Use standard Python packaging conventions
