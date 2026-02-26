# Project Setup Tool - ROADMAP

## Phase 1: Foundation (v0.1)
- [x] Discrete tool architecture
- [x] Python-only support
- [x] Basic git (new/existing/none)
- [x] Venv setup with uv
- [x] CLI config for opencode/claude
- [x] Interactive + flag mode

## Phase 2: Language Expansion (v0.2)
- [ ] JavaScript/TypeScript support
  - [ ] npm/yarn/pnpm project initialization
  - [ ] TypeScript templates
- [ ] Rust support
  - [ ] Cargo project creation
- [ ] Go support

## Phase 3: Package Managers (v0.3)
- [ ] Poetry support
- [ ] Pipenv support
- [ ] npm/yarn/pnpm (for JS)

## Phase 4: Remote Integration (v0.4)
- [ ] GitHub API integration - create remote repo
- [ ] GitLab API integration
- [ ] Auto-push after setup

## Phase 5: Templates & Structure (v0.5)
- [ ] Project structure templates
  - [ ] Library layout
  - [ ] CLI application
  - [ ] Web API (FastAPI, Flask)
  - [ ] Web application (React, Vue)
- [ ] Custom template support
- [ ] Template profiles (save/load)

## Phase 6: CI/CD & DevOps (v0.6)
- [ ] GitHub Actions templates
- [ ] GitLab CI templates
- [ ] GitHub Actions workflow for the tool itself

## Phase 7: Docker & Containers (v0.7)
- [ ] Dockerfile generation
- [ ] docker-compose.yml
- [ ] Development container configs

## Phase 8: Additional Features (v0.8)
- [ ] License selection (MIT, Apache, GPL, etc.)
- [ ] .env template generation
- [ ] .env.example for common patterns

## Phase 9: Polish & Distribution (v0.9)
- [ ] Persistent profiles/settings
- [ ] Team configurations
- [ ] Installation via pip
- [ ] Shell completion

## Future Considerations
- AI-powered template suggestions based on project description
- Integration with cloud IDEs (GitHub Codespaces, etc.)
- Team template library (internal company templates)
- Pre-commit hook setup
- Security scanning integration
