"""Virtual environment setup CLI command."""

import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

import typer


def check_uv_installed() -> bool:
    try:
        subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_python_installed() -> bool:
    try:
        subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_activation_command(venv_path: Path) -> str:
    if sys.platform == "win32":
        return str(venv_path / "Scripts" / "activate.bat")
    else:
        return str(venv_path / "bin" / "activate")


def update_gitignore(project_path: Path) -> None:
    gitignore_path = project_path / ".gitignore"
    if not gitignore_path.exists():
        gitignore_path.write_text("")

    content = gitignore_path.read_text()
    if ".venv/" not in content and ".venv\\" not in content:
        with open(gitignore_path, "a") as f:
            if content and not content.endswith("\n"):
                f.write("\n")
            f.write(".venv/\n")


def venv_setup(
    project_dir: Optional[str] = typer.Argument(None, help="Project directory path"),
    yes: bool = typer.Option(False, "--yes", help="Skip prompt, create venv"),
    use_uv: Optional[bool] = typer.Option(
        None, "--use-uv", help="Use uv for venv creation"
    ),
    use_python: Optional[bool] = typer.Option(
        None, "--use-python", help="Use python -m venv"
    ),
) -> None:
    is_interactive = project_dir is None or isinstance(
        project_dir, (typer.models.ArgumentInfo, typer.models.OptionInfo)
    )

    if not is_interactive:
        if isinstance(yes, typer.models.OptionInfo):
            yes = False
        if isinstance(use_uv, typer.models.OptionInfo):
            use_uv = None
        if isinstance(use_python, typer.models.OptionInfo):
            use_python = None

    if is_interactive:
        project_dir = typer.prompt("Project directory", default=".")

    if not project_dir:
        project_dir = "."

    project_path = Path(project_dir).resolve()

    if not project_path.exists():
        typer.echo(f"Error: Directory '{project_path}' does not exist", err=True)
        raise typer.Exit(code=1)

    venv_path = project_path / ".venv"
    venv_exists = venv_path.exists()

    if venv_exists:
        if yes:
            recreate = True
        else:
            response = typer.prompt(
                f".venv already exists in {project_path}. Recreate? (yes/no)",
                default="no",
            )
            recreate = response.lower() in ("yes", "y")

        if not recreate:
            typer.echo("Skipping venv creation")
            activation_cmd = get_activation_command(venv_path)
            typer.echo(f"Virtual environment already exists at: {venv_path}")
            typer.echo(f"Activate with: {activation_cmd}")
            return

        try:
            shutil.rmtree(venv_path)
        except Exception as e:
            typer.echo(f"Error removing existing venv: {e}", err=True)
            raise typer.Exit(code=1)

    if not yes and not is_interactive:
        response = typer.prompt("Create virtual environment? (yes/no)", default="yes")
        if response.lower() not in ("yes", "y"):
            typer.echo("Skipping venv creation")
            return

    if use_uv:
        if not check_uv_installed():
            typer.echo("Error: uv is not installed or not in PATH", err=True)
            raise typer.Exit(code=1)
        try:
            subprocess.run(
                ["uv", "venv", str(venv_path)],
                cwd=project_path,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            typer.echo(
                f"Error creating venv with uv: {e.stderr.decode() if e.stderr else e}",
                err=True,
            )
            raise typer.Exit(code=1)
    elif use_python:
        if not check_python_installed():
            typer.echo("Error: Python is not installed or not in PATH", err=True)
            raise typer.Exit(code=1)
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", str(venv_path)],
                cwd=project_path,
                capture_output=True,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            typer.echo(
                f"Error creating venv with python: {e.stderr.decode() if e.stderr else e}",
                err=True,
            )
            raise typer.Exit(code=1)
    else:
        if check_uv_installed():
            try:
                subprocess.run(
                    ["uv", "venv", str(venv_path)],
                    cwd=project_path,
                    capture_output=True,
                    check=True,
                )
            except subprocess.CalledProcessError:
                if not check_python_installed():
                    typer.echo("Error: Neither uv nor python is available", err=True)
                    raise typer.Exit(code=1)
                try:
                    subprocess.run(
                        [sys.executable, "-m", "venv", str(venv_path)],
                        cwd=project_path,
                        capture_output=True,
                        check=True,
                    )
                except subprocess.CalledProcessError as e:
                    typer.echo(
                        f"Error creating venv: {e.stderr.decode() if e.stderr else e}",
                        err=True,
                    )
                    raise typer.Exit(code=1)
        else:
            if not check_python_installed():
                typer.echo("Error: Python is not installed or not in PATH", err=True)
                raise typer.Exit(code=1)
            try:
                subprocess.run(
                    [sys.executable, "-m", "venv", str(venv_path)],
                    cwd=project_path,
                    capture_output=True,
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                typer.echo(
                    f"Error creating venv: {e.stderr.decode() if e.stderr else e}",
                    err=True,
                )
                raise typer.Exit(code=1)

    update_gitignore(project_path)

    activation_cmd = get_activation_command(venv_path)

    typer.echo(f"Virtual environment created at: {venv_path}")
    if sys.platform == "win32":
        typer.echo(f"Activate with: {activation_cmd}")
    else:
        typer.echo(f"Activate with: source {activation_cmd}")
