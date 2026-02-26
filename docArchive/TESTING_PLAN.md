# Testing Plan

## Overview
This plan outlines unit and end-to-end tests for the project-setup CLI tool.

## Prerequisites
- pytest installed: `pip install pytest`
- Run from project root: `cd D:\python\GIT\ProjectSetup`
- **Important**: Use `python -m pytest tests/` (include the `tests/` path) to avoid module import errors

---

## Phase 1: Test Infrastructure Setup

### 1.1 Install pytest
```bash
pip install pytest
```

### 1.2 Create test configuration
Create `tests/pytest.ini`:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
```

---

## Phase 2: Unit Tests

### 2.1 `tests/test_git_setup.py`
- Test git initialization with template selection
- Test git clone functionality (mock subprocess)
- Test .gitignore template generation
- Test argument parsing for new/existing/none modes

### 2.2 `tests/test_venv_setup.py`
- Test venv creation with uv (when available)
- Test venv creation with python -m venv
- Test .gitignore update
- Test existing .venv handling

### 2.3 `tests/test_cli_config.py`
- Test opencode config generation
- Test claude config generation
- Test handoff plugin creation
- Test config file structure

### 2.4 `tests/test_orchestrator.py`
- Test module chaining logic
- Test flag passing between modules
- Test error handling

---

## Phase 3: End-to-End Tests

### 3.1 Basic E2E Test
```bash
python -m project_setup project-init --git none --name e2e-test-basic --no-venv --no-pytest
```

### 3.2 Full Stack E2E Test
```bash
python -m project_setup project-init --git new --name e2e-test-full --private --venv --cli opencode --server local --workflow agentic --pytest
```

### 3.3 CLI Config E2E Test
```bash
python -m project_setup cli-config test-project --workflow assisted --cli both --server server --include-handoff
```

### 3.4 Venv Setup E2E Test
```bash
python -m project_setup venv-setup test-project --yes
```

---

## Phase 4: Verification Checklist

- [x] All unit tests pass
- [x] E2E tests create expected directory structure
- [x] Config files are valid JSON
- [x] .gitignore contains expected entries
- [x] pytest.ini or pyproject.toml has test config
- [x] Clean up test artifacts after running

---

## Notes
- Use `python -m pytest tests/` to run tests (includes the `tests/` path to avoid import errors)
- Use `pytest --collect-only` to list tests without running
- Use `python -m pytest tests/ -v` for verbose output
- Mock subprocess calls in unit tests to avoid actual git/venv operations
- E2E tests create real files - clean up with: `rm -rf e2e-test-basic e2e-test-full test-project test-venv-project`
