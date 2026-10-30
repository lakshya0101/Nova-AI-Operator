# Contributing to NOVA

We welcome contributions to NOVA – Personal AI Operating System!

## Guidelines
1. **Safety First**: Never bypass Human-in-the-Loop checkpoints for state-changing operations.
2. **Backwards Compatibility**: Ensure all existing tests pass before opening a Pull Request (`pytest -v`).
3. **Structured Schemas**: When extending agents or tools, define validated Pydantic schemas.
4. **Code Quality**: Follow PEP 8 for Python and standard TypeScript/React conventions for Next.js.

## Pull Request Process
1. Fork or branch from `main`.
2. Implement your feature or bug fix.
3. Add corresponding unit or integration tests under `backend/tests/`.
4. Ensure all tests pass: `pytest -v`.
5. Submit a pull request detailing the changes and test results.

