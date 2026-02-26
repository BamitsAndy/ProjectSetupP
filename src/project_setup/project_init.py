"""Project initialization orchestrator."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer


def run_git_setup(
    project_name: Optional[str],
    git_mode: Optional[str],
    url: Optional[str],
    public: Optional[bool],
    private: Optional[bool],
    description: Optional[str],
    include_gitignore: Optional[bool],
    include_readme: Optional[bool],
    template: Optional[str],
    is_interactive: bool,
) -> str:
    """Run git-setup and return the project path."""
    cmd = [sys.executable, "-m", "project_setup", "git-setup"]

    if project_name:
        cmd.append(project_name)

    if git_mode:
        cmd.extend(["--mode", git_mode])
    if url:
        cmd.extend(["--url", url])
    if public:
        cmd.append("--public")
    if private:
        cmd.append("--private")
    if description:
        cmd.extend(["--description", description])
    if include_gitignore:
        cmd.append("--include-gitignore")
    if include_readme:
        cmd.append("--include-readme")
    if template:
        cmd.extend(["--template", template])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        typer.echo(f"Error in git-setup: {result.stderr}", err=True)
        raise typer.Exit(code=1)

    project_path = result.stdout.strip()
    if not project_path:
        typer.echo("Error: git-setup did not return a project path", err=True)
        raise typer.Exit(code=1)

    return project_path


def run_venv_setup(
    project_dir: str,
    yes: bool,
    use_uv: Optional[bool],
    use_python: Optional[bool],
) -> None:
    """Run venv-setup."""
    cmd = [sys.executable, "-m", "project_setup", "venv-setup", project_dir]

    if yes:
        cmd.append("--yes")
    if use_uv:
        cmd.append("--use-uv")
    if use_python:
        cmd.append("--use-python")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        typer.echo(f"Error in venv-setup: {result.stderr}", err=True)
        raise typer.Exit(code=1)


def run_cli_config(
    project_dir: str,
    workflow: Optional[str],
    cli: Optional[str],
    server: Optional[str],
    include_handoff: bool,
    is_interactive: bool,
) -> None:
    """Run cli-config."""
    cmd = [sys.executable, "-m", "project_setup", "cli-config", project_dir]

    if workflow:
        cmd.extend(["--workflow", workflow])
    if cli:
        cmd.extend(["--cli", cli])
    if server:
        cmd.extend(["--server", server])
    if include_handoff:
        cmd.append("--include-handoff")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        typer.echo(f"Error in cli-config: {result.stderr}", err=True)
        raise typer.Exit(code=1)


def create_ide_config(project_path: Path) -> None:
    """Create IDE configuration files."""
    vscode_dir = project_path / ".vscode"
    vscode_dir.mkdir(exist_ok=True)

    vscode_settings = {
        "python.defaultInterpreterPath": ".venv/Scripts/python.exe"
        if sys.platform == "win32"
        else ".venv/bin/python",
        "python.analysis.typeCheckingMode": "basic",
        "editor.formatOnSave": True,
        "editor.codeActionsOnSave": {
            "source.organizeImports": True,
        },
    }

    settings_file = vscode_dir / "settings.json"
    with open(settings_file, "w") as f:
        json.dump(vscode_settings, f, indent=2)
    typer.echo(f"Created: {settings_file}")

    editorconfig_content = """root = true

[*]
indent_style = space
indent_size = 4
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.{json,yaml,yml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
"""

    editorconfig_file = project_path / ".editorconfig"
    with open(editorconfig_file, "w") as f:
        f.write(editorconfig_content)
    typer.echo(f"Created: {editorconfig_file}")


def setup_pytest(project_path: Path) -> None:
    """Set up pytest for the project."""
    tests_dir = project_path / "tests"
    tests_dir.mkdir(exist_ok=True)

    init_file = tests_dir / "__init__.py"
    init_file.touch()

    test_file = tests_dir / "test_example.py"
    test_file.write_text('''"""Example test file."""

def test_example():
    """Example test."""
    assert True
''')
    typer.echo(f"Created: {test_file}")

    pytest_ini = project_path / "pytest.ini"
    pytest_ini.write_text("""[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
""")
    typer.echo(f"Created: {pytest_ini}")


def git_add_and_commit(project_path: Path) -> None:
    """Add all files and commit."""
    try:
        subprocess.run(
            ["git", "add", "."],
            cwd=project_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial project setup"],
            cwd=project_path,
            capture_output=True,
            check=True,
        )
        typer.echo("Git commit created: 'Initial project setup'")
    except subprocess.CalledProcessError as e:
        typer.echo(f"Warning: Git commit failed: {e}", err=True)


def project_init(
    git: Optional[str] = typer.Option(
        None, "--git", help="Git mode: new, existing, or none"
    ),
    name: Optional[str] = typer.Option(None, "--name", help="Project name"),
    url: Optional[str] = typer.Option(
        None, "--url", help="Repository URL for existing mode"
    ),
    public: Optional[bool] = typer.Option(None, "--public", help="Public repository"),
    private: Optional[bool] = typer.Option(
        None, "--private", help="Private repository"
    ),
    venv: Optional[bool] = typer.Option(
        None, "--venv", help="Create virtual environment"
    ),
    no_venv: Optional[bool] = typer.Option(
        None, "--no-venv", help="Skip virtual environment creation"
    ),
    cli: Optional[str] = typer.Option(
        None, "--cli", help="CLI tool: opencode, claude, or both"
    ),
    server: Optional[str] = typer.Option(
        None, "--server", help="Server mode for opencode: local or server"
    ),
    workflow: Optional[str] = typer.Option(
        None, "--workflow", help="Workflow type: agentic or assisted"
    ),
    pytest: Optional[bool] = typer.Option(
        None, "--pytest", help="Set up pytest testing"
    ),
    no_pytest: Optional[bool] = typer.Option(
        None, "--no-pytest", help="Skip pytest setup"
    ),
) -> None:
    """Initialize a complete project with all modules."""

    is_interactive = (
        git is None or name is None or isinstance(git, typer.models.OptionInfo)
    )

    if not is_interactive:
        if isinstance(git, typer.models.OptionInfo):
            git = None
        if isinstance(public, typer.models.OptionInfo):
            public = None
        if isinstance(private, typer.models.OptionInfo):
            private = None
        if isinstance(venv, typer.models.OptionInfo):
            venv = None
        if isinstance(no_venv, typer.models.OptionInfo):
            no_venv = None
        if isinstance(cli, typer.models.OptionInfo):
            cli = None
        if isinstance(server, typer.models.OptionInfo):
            server = None
        if isinstance(workflow, typer.models.OptionInfo):
            workflow = None
        if isinstance(pytest, typer.models.OptionInfo):
            pytest = None
        if isinstance(no_pytest, typer.models.OptionInfo):
            no_pytest = None

    if is_interactive:
        typer.echo("=== Project Initialization ===\n")

        git = typer.prompt("Git mode (new/existing/none)", default="new")

        if git == "new":
            name = typer.prompt("Project name")

            visibility = typer.prompt("Visibility (public/private)", default="private")
            is_private = visibility == "private"

            description = typer.prompt("Description (optional)", default="")

            include_gitignore = typer.prompt("Include .gitignore?", default=True)
            include_readme = typer.prompt("Include README?", default=True)

            if include_gitignore:
                template = typer.prompt(
                    "Gitignore template (Python/Node/Rust/Go/Blank)", default="Python"
                )
            else:
                template = None
        elif git == "existing":
            url = typer.prompt("Repository URL")
            name = typer.prompt(
                "Project name (optional, leave empty to derive from URL)", default=""
            )
            name = name if name else None
        else:
            name = typer.prompt("Project name")

        create_venv = typer.prompt("Create virtual environment?", default=True)

        cli = typer.prompt("Primary CLI tool (opencode/claude/both)", default="both")

        workflow = typer.prompt("Workflow type (agentic/assisted)", default="assisted")

        if cli in ("opencode", "both"):
            server = typer.prompt(
                "Opencode server mode (local/server)", default="local"
            )

        if cli == "both":
            include_handoff = typer.prompt("Include handoff plugin? (y/n)", default="n")
            include_handoff = include_handoff.lower() in ("y", "yes")
        else:
            include_handoff = False

        use_pytest = typer.prompt("Set up pytest testing?", default=True)

        typer.echo("")
    else:
        create_venv = (
            venv if venv is not None else (not no_venv if no_venv is not None else True)
        )
        use_pytest = (
            pytest
            if pytest is not None
            else (not no_pytest if no_pytest is not None else False)
        )
        include_handoff = False
        include_gitignore = True
        include_readme = True
        template = "Python"
        is_private = private if private is not None else True
        description = None

        if git == "none":
            create_venv = False
            use_pytest = False
            cli = "both"
            workflow = "assisted"

    typer.echo("--- Step 1: Git Setup ---")
    project_path = run_git_setup(
        project_name=name,
        git_mode=git,
        url=url,
        public=is_private if not is_interactive and public is None else public,
        private=is_private if not is_interactive and private is None else private,
        description=description,
        include_gitignore=include_gitignore,
        include_readme=include_readme,
        template=template,
        is_interactive=is_interactive,
    )
    typer.echo(f"Project created at: {project_path}\n")

    project_path_obj = Path(project_path)

    if create_venv:
        typer.echo("--- Step 2: Virtual Environment ---")
        run_venv_setup(
            project_dir=project_path,
            yes=True,
            use_uv=None,
            use_python=None,
        )
        typer.echo("")

    typer.echo("--- Step 3: CLI Configuration ---")
    run_cli_config(
        project_dir=project_path,
        workflow=workflow,
        cli=cli,
        server=server,
        include_handoff=include_handoff,
        is_interactive=is_interactive,
    )
    typer.echo("")

    typer.echo("--- Step 4: IDE Configuration ---")
    create_ide_config(project_path_obj)
    typer.echo("")

    if use_pytest:
        typer.echo("--- Step 5: Testing Setup ---")
        setup_pytest(project_path_obj)
        typer.echo("")

    if git in ("new", "existing"):
        typer.echo("--- Step 6: Git Commit ---")
        git_add_and_commit(project_path_obj)
        typer.echo("")

    typer.echo("=== Project Initialization Complete! ===\n")
    typer.echo(f"Project: {project_path}")

    if create_venv:
        venv_path = project_path_obj / ".venv"
        if venv_path.exists():
            if sys.platform == "win32":
                typer.echo(f"Activate venv: {venv_path}\\Scripts\\activate.bat")
            else:
                typer.echo(f"Activate venv: source {venv_path}/bin/activate")

    typer.echo("\nNext steps:")
    typer.echo(f"  cd {project_path}")
    if create_venv:
        if sys.platform == "win32":
            typer.echo(f"  {project_path}\\.venv\\Scripts\\activate.bat")
        else:
            typer.echo(f"  source {project_path}/.venv/bin/activate")


if __name__ == "__main__":
    typer.run(project_init)


def main() -> None:
    """Entry point for the project-init CLI command."""
    typer.run(project_init)
