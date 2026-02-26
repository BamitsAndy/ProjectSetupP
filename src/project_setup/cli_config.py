"""CLI configuration command."""

import json
from pathlib import Path
from typing import Optional

import typer


def cli_config(
    project_dir: Optional[str] = None,
    workflow: Optional[str] = None,
    cli: Optional[str] = None,
    server: Optional[str] = None,
    include_handoff: bool = False,
) -> None:
    """Configure CLI tools (opencode, claude) for a project."""
    is_interactive = (
        workflow is None
        or cli is None
        or isinstance(workflow, typer.models.OptionInfo)
        or isinstance(cli, typer.models.OptionInfo)
    )

    if project_dir is None or isinstance(project_dir, type(typer.models.ArgumentInfo)):
        project_dir = typer.prompt("Project directory path", default=str(Path.cwd()))

    project_path = Path(project_dir)

    if not project_path.exists():
        typer.echo(f"Error: Directory '{project_path}' does not exist", err=True)
        raise typer.Exit(code=1)

    if is_interactive:
        workflow_input = typer.prompt(
            "Workflow type (agentic/assisted)",
            default="assisted",
        )
        workflow = workflow_input if workflow_input else "assisted"

        cli_input = typer.prompt(
            "Primary CLI tool (opencode/claude/both)",
            default="both",
        )
        cli = cli_input if cli_input else "both"
    else:
        if workflow is None:
            workflow = "assisted"
        if cli is None:
            cli = "both"

    if cli in ("opencode", "both"):
        if is_interactive:
            server_input = typer.prompt(
                "Opencode server mode (local/server)",
                default="local",
            )
            server = server_input if server_input else "local"
        else:
            if server is None:
                server = "local"

        opencode_config = {
            "server": server,
            "workflow": workflow,
        }

        opencode_dir = project_path / ".opencode"
        opencode_dir.mkdir(parents=True, exist_ok=True)

        settings_file = opencode_dir / "settings.json"
        with open(settings_file, "w") as f:
            json.dump(opencode_config, f, indent=2)

        typer.echo(f"Created: {settings_file}")

        if is_interactive:
            include_init = typer.prompt(
                "Create /init command script? (y/n)",
                default="n",
            )
            if include_init.lower() in ("y", "yes"):
                commands_dir = opencode_dir / "commands"
                commands_dir.mkdir(exist_ok=True)
                init_file = commands_dir / "init.py"
                init_file.write_text(
                    '#!/usr/bin/env python3\n"""Init command for opencode."""\n\n'
                )
                typer.echo(f"Created: {init_file}")

    if cli in ("claude", "both"):
        claude_config = {
            "workflow": workflow,
        }

        claude_dir = project_path / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)

        settings_file = claude_dir / "settings.json"
        with open(settings_file, "w") as f:
            json.dump(claude_config, f, indent=2)

        typer.echo(f"Created: {settings_file}")

    if cli == "both":
        if is_interactive:
            handoff_input = typer.prompt(
                "Include handoff plugin? (y/n)",
                default="n",
            )
            include_handoff = handoff_input.lower() in ("y", "yes")

        if include_handoff:
            mcp_dir = project_path / ".opencode" / "mcp"
            mcp_dir.mkdir(parents=True, exist_ok=True)
            handoff_file = mcp_dir / "handoff.py"
            handoff_file.write_text(
                "# Handoff plugin placeholder\n# This is a ROADMAP item for future implementation\n"
            )
            typer.echo(f"Created: {handoff_file}")

    typer.echo("CLI configuration complete!")
