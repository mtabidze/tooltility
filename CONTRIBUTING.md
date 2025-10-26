### Contributing to Tooltility

Thanks for your interest in contributing! This project aims to provide safe, internal-friendly utilities built with Streamlit.

### Ways to contribute
- **Bug reports**: Open an issue describing the problem and how to reproduce it.
- **Feature requests**: Open an issue explaining the use case and proposed solution.
- **Pull requests**: Fork the repo and submit a PR following the guidelines below.

### Pull request guidelines
- Create a topic branch from `main`.
- Keep changes focused and incremental. Add tests for new behavior.
- Run the full quality suite locally before pushing:
  ```bash
  poetry install --with dev
  poetry run make run-all-tests
  ```
- Ensure `ruff`, `mypy`, and tests pass; maintain or improve coverage.

### Code style
- Python 3.14-compatible, typed where practical.
- Formatting and linting via Ruff; type checking via mypy.

### Security
Do not include secrets in issues or PRs. To report security concerns, please open an issue (see `SECURITY.md`).

### License
By contributing, you agree that your contributions will be licensed under the MIT License.


