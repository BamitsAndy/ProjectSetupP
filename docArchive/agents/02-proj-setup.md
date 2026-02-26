# Agent 2: proj-setup Module

## Task
Implement the `proj-setup` module for project folder scaffolding.

## Working Directory
`D:\python\GIT\ProjectSetup`

## Context
This module should create a project folder. It will be called by `project-init` orchestrator or used standalone.

## Requirements

### Functionality
1. Accept project name as argument
2. Accept target directory (optional, default: current directory)
3. Create the project folder
4. Ask user for structure type: `flat` or `src/` layout
5. Create basic structure:
   - `flat`: just the folder with `__init__.py`
   - `src/`: creates `src/` and `src/__init__.py`

### CLI Interface (using typer)
```bash
proj-setup <project_name> [--path PATH] [--flat | --src]
```

- `--path`: Target directory (default: current)
- `--flat`: Flat structure (no src/)
- `--src`: Use src/ structure (default)

### Interactive Mode
If no project name provided, prompt for:
- Project name
- Target directory (default: current)
- Structure type

### Output
- Print created folder path to stdout
- Exit 0 on success, non-zero on error

## Implementation
Edit `src/project_setup/proj_setup.py`

## Verification
```bash
python -m project_setup proj-setup test-project --flat
# Should create test-project/ folder
ls test-project/
```

## Notes
- Keep it simple - folder creation only
- Use typer for CLI
- Subprocess calls not needed here
