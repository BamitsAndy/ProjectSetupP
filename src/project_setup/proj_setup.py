"""Project setup CLI command."""

from pathlib import Path
from typing import Optional

import typer

from project_setup.git_setup import git_setup
from project_setup.venv_setup import venv_setup
from project_setup.cli_config import cli_config
from project_setup.project_init import project_init

app = typer.Typer()


@app.command(name="proj-setup")
def proj_setup(
    project_name: Optional[str] = typer.Argument(
        None, help="Name of the project to create"
    ),
    path: Optional[str] = typer.Option(
        None, "--path", "-p", help="Target directory (default: current)"
    ),
    flat: bool = typer.Option(False, "--flat", help="Flat structure (no src/)"),
    src: bool = typer.Option(True, "--src", help="Use src/ structure (default)"),
) -> None:
    if flat and src:
        src = False

    is_interactive = project_name is None or isinstance(
        project_name, (typer.models.ArgumentInfo, typer.models.OptionInfo)
    )

    if not is_interactive:
        if isinstance(path, typer.models.OptionInfo):
            path = None
        if isinstance(flat, typer.models.OptionInfo):
            flat = False
        if isinstance(src, typer.models.OptionInfo):
            src = True

    if is_interactive:
        project_name = typer.prompt("Project name")
        path_input = typer.prompt(
            "Target directory (leave empty for current)",
            default="",
        )
        path = path_input if path_input else str(Path.cwd())
        structure = typer.prompt(
            "Structure type (flat/src)",
            default="src",
        )
        flat = structure == "flat"
        src = structure == "src"

    if path is None or path == "":
        path_obj = Path.cwd()
    else:
        path_obj = Path(path)

    project_path = path_obj / project_name

    if project_path.exists():
        typer.echo(f"Error: Directory '{project_path}' already exists", err=True)
        raise typer.Exit(code=1)

    try:
        project_path.mkdir(parents=True)
    except Exception as e:
        typer.echo(f"Error creating directory: {e}", err=True)
        raise typer.Exit(code=1)

    if flat:
        init_file = project_path / "__init__.py"
        init_file.touch()
    else:
        src_dir = project_path / "src"
        src_dir.mkdir(exist_ok=True)
        init_file = src_dir / "__init__.py"
        init_file.touch()

    typer.echo(project_path)


@app.command(name="git-setup")
def git_setup_cmd(
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
    git_setup(
        project_name=project_name,
        mode=mode,
        url=url,
        public=public,
        private=private,
        description=description,
        include_gitignore=include_gitignore,
        include_readme=include_readme,
        template=template,
    )


@app.command(name="venv-setup")
def venv_setup_cmd(
    project_dir: Optional[str] = typer.Argument(None, help="Project directory path"),
    yes: bool = typer.Option(False, "--yes", help="Skip prompt, create venv"),
    use_uv: Optional[bool] = typer.Option(
        None, "--use-uv", help="Use uv for venv creation"
    ),
    use_python: Optional[bool] = typer.Option(
        None, "--use-python", help="Use python -m venv"
    ),
) -> None:
    venv_setup(
        project_dir=project_dir,
        yes=yes,
        use_uv=use_uv,
        use_python=use_python,
    )


@app.command(name="cli-config")
def cli_config_cmd(
    project_dir: Optional[str] = typer.Argument(None, help="Project directory path"),
    workflow: Optional[str] = typer.Option(
        None, "--workflow", help="Workflow type: agentic or assisted"
    ),
    cli: Optional[str] = typer.Option(
        None, "--cli", help="CLI tool: opencode, claude, or both"
    ),
    server: Optional[str] = typer.Option(
        None, "--server", help="Server mode for opencode: local or server"
    ),
    include_handoff: bool = typer.Option(
        False, "--include-handoff", help="Include handoff plugin"
    ),
) -> None:
    cli_config(
        project_dir=project_dir,
        workflow=workflow,
        cli=cli,
        server=server,
        include_handoff=include_handoff,
    )


@app.command(name="project-init")
def project_init_cmd(
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
    project_init(
        git=git,
        name=name,
        url=url,
        public=public,
        private=private,
        venv=venv,
        no_venv=no_venv,
        cli=cli,
        server=server,
        workflow=workflow,
        pytest=pytest,
        no_pytest=no_pytest,
    )


if __name__ == "__main__":
    app()
