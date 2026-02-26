# Agent 6: project-init Orchestrator

## Task
Implement the `project-init` module - the main orchestrator that chains all other modules.

## Working Directory
`D:\python\GIT\ProjectSetup`

## Context
This is the main entry point. It calls the other modules in sequence and manages the overall flow.

## Requirements

### Full Workflow
1. **Git Setup** - Call git-setup (or prompt for git choice)
2. **Project Folder** - Ensure folder exists (use proj-setup if needed)
3. **cd into folder** - All subsequent ops in project directory
4. **Venv Setup** - Call venv-setup
5. **CLI Config** - Call cli-config
6. **IDE Config** - Create `.vscode/settings.json`, `.editorconfig`
7. **Testing** - Prompt for pytest, create basic test structure if yes
8. **Git Update** - If git enabled: add all, commit with message "Initial project setup"

### CLI Interface
```bash
project-init [--git new|existing|none] [--name NAME] [--url REPO_URL] [--public | --private] [--venv | --no-venv] [--cli opencode|claude|both] [--server local|server] [--workflow agentic|assisted] [--pytest | --no-pytest]
```

All flags are optional - if not provided, prompt interactively.

### Interactive Mode Prompts
1. Git mode (new/existing/none)
2. Project name
3. If new: public/private, description, gitignore, readme, template
4. If existing: repo URL
5. Create venv? (yes)
6. Primary CLI (opencode/claude/both)
7. Workflow type
8. If opencode: server/local
9. If both: include handoff?
10. Testing framework (pytest/none)

### Output
- Print summary of what was created
- Print next steps (activation command, etc.)
- Exit 0 on success

## Implementation
Edit `src/project_setup/project_init.py`

Use subprocess to call other modules:
```python
subprocess.run(["python", "-m", "project_setup", "git-setup", ...])
```

### Handling Project Directory
- git-setup returns the project directory path
- Store this and pass to subsequent modules
- Use `workdir` parameter in subprocess

## Verification
```bash
python -m project_setup project-init
# Should prompt through full workflow
# Or test with flags:
python -m project_setup project-init --git new --name testproj --private --venv --cli opencode --server local --workflow agentic --pytest
```

## Notes
- This is the main user-facing command
- Make prompts clear and helpful
- Provide sensible defaults where possible
- Print progress as things happen
