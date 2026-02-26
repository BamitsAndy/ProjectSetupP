"""Git setup CLI command."""

import subprocess
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import typer

GITIGNORE_TEMPLATES = {
    "Python": """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
.venv/
env/
.env
.pytest_cache/
.coverage
htmlcov/
*.log
""",
    "Node": """node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock
.env
.env.local
dist/
build/
.DS_Store
*.log
coverage/
.nyc_output/
""",
    "Rust": """target/
Cargo.lock
*.rs.bk
*.pdb
.DS_Store
""",
    "Go": """*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
go.sum
.DS_Store
*.log
""",
    "Blank": """*
""",
}


def check_git_installed() -> bool:
    try:
        subprocess.run(
            ["git", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_gitignore_template(template_name: str) -> str:
    return GITIGNORE_TEMPLATES.get(template_name, GITIGNORE_TEMPLATES["Blank"])


def create_project_directory(project_path: Path) -> None:
    if project_path.exists():
        typer.echo(f"Error: Directory '{project_path}' already exists", err=True)
        raise typer.Exit(code=1)

    try:
        project_path.mkdir(parents=True)
    except Exception as e:
        typer.echo(f"Error creating directory: {e}", err=True)
        raise typer.Exit(code=1)


def git_setup(
    project_name: Optional[str] = typer.Argument(
        None, help="Name of the project (for new mode)"
    ),
    mode: Optional[str] = typer.Option(
        None, "--mode", help="Mode: new, existing, or none"
    ),
    url: Optional[str] = typer.Option(
        None, "--url", help="Repository URL for existing mode"
    ),
    public: Optional[bool] = typer.Option(None, "--public", help="Public repository"),
    private: Optional[bool] = typer.Option(
        None, "--private", help="Private repository"
    ),
    description: Optional[str] = typer.Option(
        None, "--description", help="Project description"
    ),
    include_gitignore: Optional[bool] = typer.Option(
        None, "--include-gitignore", help="Include .gitignore file"
    ),
    include_readme: Optional[bool] = typer.Option(
        None, "--include-readme", help="Include README.md file"
    ),
    template: Optional[str] = typer.Option(
        None, "--template", help="Gitignore template: Python, Node, Rust, Go, Blank"
    ),
) -> None:
    if not check_git_installed():
        typer.echo("Error: git is not installed or not in PATH", err=True)
        raise typer.Exit(code=1)

    is_interactive = mode is None or isinstance(
        mode, (typer.models.OptionInfo, type(None))
    )

    if not is_interactive:
        if isinstance(mode, typer.models.OptionInfo):
            mode = None
        if isinstance(public, typer.models.OptionInfo):
            public = None
        if isinstance(private, typer.models.OptionInfo):
            private = None
        if isinstance(include_gitignore, typer.models.OptionInfo):
            include_gitignore = None
        if isinstance(include_readme, typer.models.OptionInfo):
            include_readme = None

    if is_interactive:
        mode = typer.prompt("Git mode (new/existing/none)", default="new")

    if mode is None:
        mode = "none"

    if mode not in ("new", "existing", "none"):
        typer.echo(
            f"Error: Invalid mode '{mode}'. Use new, existing, or none.", err=True
        )
        raise typer.Exit(code=1)

    if mode == "none":
        if not project_name:
            if is_interactive:
                project_name = typer.prompt("Project name")
            else:
                typer.echo(
                    "Error: project_name is required in non-interactive mode", err=True
                )
                raise typer.Exit(code=1)

        project_path = Path.cwd() / project_name

        create_project_directory(project_path)

        typer.echo(project_path)

    if mode == "new":
        if not project_name:
            if is_interactive:
                project_name = typer.prompt("Project name")
            else:
                typer.echo(
                    "Error: project_name is required in non-interactive mode", err=True
                )
                raise typer.Exit(code=1)

        if public is None and private is None:
            if is_interactive:
                visibility = typer.prompt(
                    "Visibility (public/private)", default="private"
                )
                is_private = visibility == "private"
            else:
                is_private = True
        else:
            is_private = private if private is not None else False

        if is_interactive and not description:
            description = typer.prompt("Description (optional)", default="")

        if include_gitignore is None:
            if is_interactive:
                include_gitignore = typer.prompt("Include .gitignore?", default=True)
            else:
                include_gitignore = False

        if include_gitignore and not template:
            if is_interactive:
                template = typer.prompt(
                    "Gitignore template (Python/Node/Rust/Go/Blank)", default="Python"
                )
            else:
                template = "Python"

        project_path = Path.cwd() / project_name

        create_project_directory(project_path)

        try:
            subprocess.run(
                ["git", "init"],
                cwd=project_path,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            typer.echo(
                f"Error running git init: {e.stderr.decode() if e.stderr else e}",
                err=True,
            )
            raise typer.Exit(code=1)

        if include_gitignore:
            template_name = template if template else "Python"
            gitignore_content = get_gitignore_template(template_name)
            gitignore_path = project_path / ".gitignore"
            gitignore_path.write_text(gitignore_content)

        if include_readme:
            readme_content = f"# {project_name}\n\n"
            if description:
                readme_content += f"{description}\n"
            readme_path = project_path / "README.md"
            readme_path.write_text(readme_content)

        try:
            subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                capture_output=True,
                check=True,
            )
            subprocess.run(
                ["git", "commit", "-m", "Initial commit"],
                cwd=project_path,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            typer.echo(
                f"Error during git commit: {e.stderr.decode() if e.stderr else e}",
                err=True,
            )
            raise typer.Exit(code=1)

        typer.echo(project_path)

    elif mode == "existing":
        if not url:
            if is_interactive:
                url = typer.prompt("Repository URL")
            else:
                typer.echo("Error: --url is required in non-interactive mode", err=True)
                raise typer.Exit(code=1)

        target_folder = None
        if not is_interactive:
            if project_name:
                target_folder = project_name

        if not target_folder:
            parsed = urlparse(url)
            path_parts = parsed.path.strip("/").split("/")
            if path_parts:
                repo_name = path_parts[-1]
                if repo_name.endswith(".git"):
                    repo_name = repo_name[:-4]
                if is_interactive:
                    target_folder = typer.prompt(
                        "Target folder name", default=repo_name
                    )
                else:
                    target_folder = repo_name
            else:
                if is_interactive:
                    target_folder = typer.prompt("Target folder name")
                else:
                    typer.echo(
                        "Error: Could not determine target folder name", err=True
                    )
                    raise typer.Exit(code=1)

        target_path = Path.cwd() / target_folder

        if target_path.exists():
            typer.echo(f"Error: Directory '{target_path}' already exists", err=True)
            raise typer.Exit(code=1)

        try:
            subprocess.run(
                ["git", "clone", url, str(target_path)],
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            typer.echo(
                f"Error cloning repository: {e.stderr.decode() if e.stderr else e}",
                err=True,
            )
            raise typer.Exit(code=1)

        typer.echo(target_path)
