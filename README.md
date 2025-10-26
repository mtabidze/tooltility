### Tooltility

A lightweight internal web app of small, safe utilities built with Streamlit. It helps you perform common tasks entirely inside your network so data never leaves your environment.

- **Framework**: Streamlit
- **Language**: Python 3.14+
- **Dependency management**: Poetry
- **License**: MIT

---

### Quick start

- **Prerequisites**:
  - Python 3.14+
  - Poetry

- **Install**:
```bash
poetry install --with dev
```

- **Run the app**:
```bash
streamlit run app/src/streamlit_app.py
```

The app starts on `http://localhost:8501`.

---

### Running with Docker

Build and run the container:
```bash
docker build -t tooltility .
docker run --rm -p 8501:8501 tooltility
```

- The container exposes port `8501` and runs `streamlit_app.py`.
- A container healthcheck calls `http://localhost:8501/_stcore/health`.
  - Exit status meanings: 0 = healthy; 1 = unhealthy; 2 = reserved.

You can also run the healthcheck script manually inside the container:
```bash
python healthcheck.py http://localhost:8501/_stcore/health
```

---

### Scripts and developer workflow

- **App and tooling targets** (Makefile):
  - `make run-app`: run the Streamlit app.
  - `make run-ruff`: format and lint code with Ruff.
  - `make run-mypy`: run mypy type checking.

- **Test and quality targets** (Makefile):
  - `make run-unit-testing`: run unit tests with coverage.
  - `make run-functional-testing`: run functional tests with coverage.
  - `make run-coverage-measurement`: enforce coverage thresholds (75% for unit and functional).
  - `make run-static-code-analysis`: Ruff lint/format check, mypy, pip-licenses, pip-audit.
  - `make run-all-tests`: run all of the above and aggregate exit codes.

Coverage artifacts are written to `.cover/` with HTML reports per test type.

---

### Development notes

- Use Poetry for all dependency management and lockfile updates.
- Linting/formatting is standardized via Ruff; static typing via mypy.
- Streamlit navigation uses pages; add new tools under `app/src/pages` and supporting logic under `app/src/tools`.

---

### Healthcheck details

The healthcheck CLI performs a GET to the provided URL and prints status:
```bash
python app/src/healthcheck.py http://localhost:8501/_stcore/health
```
- Exit codes:
  - `0`: success — container healthy and ready for use
  - `1`: unhealthy — container isn't working correctly
  - `2`: reserved — do not use

---

### License

MIT. See `LICENSE`.