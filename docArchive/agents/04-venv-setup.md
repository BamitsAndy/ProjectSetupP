# Agent 4: venv-setup Module

## Task
Implement the `venv-setup` module for virtual environment creation.

## Working Directory
`D:\python\GIT\ProjectSetup`

## Context
This module creates a Python virtual environment in the project folder.

## Requirements

### Functionality
1. Accept project directory as argument (or prompt if not provided)
2. Ask user: create venv? (yes/no)
3. If yes:
   - Check if `uv` is available (preferred)
   - Fall back to `python -m venv` if uv not found
   - Create `.venv/` in project directory
   - Add `.venv/` to project's `.gitignore` if it exists
4. Output activation command

### CLI Interface
```bash
venv-setup [project_dir] [--yes] [--use-uv | --use-python]
```

- `--yes`: Skip prompt, create venv
- `--use-uv`: Use uv (default: try uv first, fall back to python)
- `--use-python`: Use python -m venv

### Output
- Print venv path to stdout
- Print activation command
- Exit 0 on success

## Implementation
Edit `src/project_setup/venv_setup.py`

Use subprocess for:
- `uv venv .venv` or `python -m venv .venv`
- Check for uv: `uv --version`

## Gitignore Update
If `.gitignore` exists, read it, add `.venv/` if not present, write back.

## Verification
```bash
python -m project_setup venv-setup ./my-project --yes
ls -la my-project/.venv/
grep ".venv" my-project/.gitignore
```

## Notes
- Handle case where project directory doesn't exist
- Handle case where .venv already exists (prompt to recreate or skip)
- Windows vs Unix activation command difference
