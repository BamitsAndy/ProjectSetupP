# Agent 5: cli-config Module

## Task
Implement the `cli-config` module for CLI tool (opencode, claude) configuration.

## Working Directory
`D:\python\GIT\ProjectSetup`

## Context
This module creates configuration files for AI CLI tools.

## Requirements

### Functionality

#### Workflow Type
Ask user: `agentic` | `assisted`

#### Primary CLI Tool
Ask user: `opencode` | `claude` | `both`

#### If opencode:
1. Server mode: `server` | `local`
2. Create `.opencode/settings.json`:
   ```json
   {
     "server": "local" | "server",
     "workflow": "agentic" | "assisted"
   }
   ```
3. If user wants `/init`, create `.opencode/commands/` with basic init script

#### If claude:
1. Create `.claude/settings.json`:
   ```json
   {
     "workflow": "agentic" | "assisted"
   }
   ```

#### If both:
1. Create both configs above
2. Ask about handoff plugin: include or not
3. If handoff: create `.opencode/mcp/handoff.py` or similar (just placeholder for now - ROADMAP item really)

### CLI Interface
```bash
cli-config [project_dir] [--workflow agentic|assisted] [--cli opencode|claude|both] [--server local|server] [--include-handoff]
```

### Output
- Print created config files to stdout
- Exit 0 on success

## Implementation
Edit `src/project_setup/cli_config.py`

Create directories and JSON files using pathlib and json.

## Verification
```bash
python -m project_setup cli-config ./my-project --workflow agentic --cli opencode --server local
cat my-project/.opencode/settings.json
ls my-project/.opencode/
```

## Notes
- Use json module for config files
- Create directories with parents=True, exist_ok=True
- Keep configs minimal - can expand later
