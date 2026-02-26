# Agent 3: git-setup Module

## Task
Implement the `git-setup` module for git initialization or cloning.

## Working Directory
`D:\python\GIT\ProjectSetup`

## Context
This module handles git operations. It may call `proj-setup` if creating a new repo.

## Requirements

### Functionality

#### Mode Selection
Ask user to choose: `new` | `existing` | `none`
- Use `--mode` flag for non-interactive

#### If `new`:
1. Project name (argument or prompt)
2. Visibility: `public` | `private`
3. Description (optional, prompt)
4. Include `.gitignore` (prompt, default: yes)
5. Include `README.md` (prompt, default: yes)
6. Gitignore template: select from common templates (Python, Node, Rust, Go, blank)
7. Create folder with `git init`
8. Create `.gitignore` from template
9. Create `README.md` with project name and description
10. Initial commit

#### If `existing`:
1. Repository URL (argument or prompt)
2. Target folder name (prompt, default: extracted from repo)
3. Clone the repository

#### If `none`:
1. Print "No git initialized" and exit
2. Return the project name provided

### CLI Interface
```bash
git-setup [--mode new|existing|none] [project_name] [--url REPO_URL] [--public | --private] [--description TEXT] [--include-gitignore] [--include-readme] [--template TEMPLATE]
```

### Output
- Print the project directory path to stdout
- Exit 0 on success

## Implementation
Edit `src/project_setup/git_setup.py`

Use subprocess to run git commands:
- `git init`
- `git clone`
- `git add .`
- `git commit`

## Gitignore Templates
Create a simple dictionary of templates in the module:
- Python: standard Python .gitignore
- Node: node_modules, package-lock.json, etc.
- Blank: just `*`

## Verification
```bash
python -m project_setup git-setup new my-git-project --private --include-gitignore --include-readme --template Python
ls my-git-project/
git -C my-git-project log
```

## Notes
- Handle errors gracefully (git not installed, network issues)
- Use pathlib for path handling
- The project folder should be created before git operations
