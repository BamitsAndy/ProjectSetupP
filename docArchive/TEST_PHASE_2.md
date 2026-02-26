# TEST PHASE 2: Unit Tests Implementation Guide
## Overview
This document provides details for implementing phase 2 unit tests. Phase 2 has been completed and all 15 unit tests passed successfully.

## Directory Structure
- `tests/`: Contains all unit test files.
- Each file should contain unittest.TestCase classes corresponding to specific code modules.

## Test File Contents and Expectations
Each test method follows this structure:
```python
@patch('module.subprocess_function')
def test_operation(self, mock_subprocess):
    # Arrange: Set up mock return values
    # Act: Call the function under test
    # Assert: Verify results match expectations
```

### Examples for Each Test File

**1. tests/test_git_setup.py**
- Tests for git initialization with templates, clone functionality, .gitignore generation, and argument parsing.
- Mock subprocess calls for functions like `subprocess.run` in actual code.

**2. tests/test_venv_setup.py**
- Tests for venv creation (with mocks), .gitignore update, and handling of existing virtual environments.
- Mock file operations if needed to isolate the logic.

**3. tests/test_cli_config.py**
- Tests for opencode config, claude config, handoff plugin creation, and config file structure validation.
- Focus on testing the logic of config generation rather than file system operations.

**4. tests/test_orchestrator.py**
- Tests for module chaining logic, flag passing between modules, and error handling.
- Mock all external dependencies to test internal workflows.

## Mocking Strategy
- Use unittest.mock.patch to replace functions that call subprocess or I/O.
- Return dummy values for normal operations and raise exceptions for expected errors in tests.
- Example:
```python
@patch('subprocess.run')
def test_operation(self, mock_subprocess):
    mock_subprocess.return_value = (0, None)  # Simulate successful operation
    # ...
```

## Important Notes
- Do not run actual git/venv operations. Use mocks to simulate them.
- Focus on testing the logic and behavior of functions without their side effects.
- Follow pytest conventions for test collection and structure (e.g., `test_*` naming).