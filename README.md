# Django + uv + Docker + Allure Example Project

This project is a Django REST API with modern Python tooling, using [uv](https://github.com/astral-sh/uv) for dependency management, GitHub Actions for CI, Docker for containerization, and Allure for test reporting.

## Features
- Django REST API (with DRF)
- Modern dependency management with uv and lockfile
- Automated testing and linting (pytest, pytest-xdist for parallelism, black, isort, pylint, bandit)
- Allure test reporting
- GitHub Actions CI workflow
- Docker support for easy deployment

---

## Getting Started

### 1. Clone the repository
```sh
git clone <your-repo-url>
cd <your-repo>
```

### 2. Install dependencies with uv
```sh
pip install uv
uv sync --all-extras --dev
```

### 3. Run migrations and start the server
```sh
uv run python api/coronavstech/manage.py migrate
uv run python api/coronavstech/manage.py runserver
```

### 4. Run tests (in parallel)
```sh
uv run pytest -v -n auto
```

### 5. Lint and format code
```sh
uv run black . --check
uv run isort . --check --diff
uv run pylint api coronavstech
uv run bandit -r api --skip B101,B105
```

### 6. Allure Test Reporting
- **Generate Allure results:**
  ```sh
  uv run pytest --alluredir=allure-results
  ```
- **View Allure report (requires Allure CLI):**
  1. [Install Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline)
  2. Run:
     ```sh
     allure serve allure-results
     ```
  This will open the Allure report in your browser.

---

## Docker

Build and run the app in Docker:

```sh
docker build -t myapp .
docker run -p 8000:8000 myapp
```

---

## Continuous Integration

- The project uses GitHub Actions for CI.
- The workflow runs tests (in parallel), linting, formatting, security checks, and dependency review on every push and pull request.

---

## Project Structure

```
api/
  coronavstech/
    manage.py
    ...
fibonacci/
Dockerfile
.dockerignore
.pyproject.toml
.venv/ (ignored)
```

---

## Useful Commands
- **Run Django server:** `uv run python api/coronavstech/manage.py runserver`
- **Run tests in parallel:** `uv run pytest -v -n auto`
- **Lint:** `uv run pylint api coronavstech`
- **Format:** `uv run black . --check`
- **Import order:** `uv run isort . --check --diff`
- **Security:** `uv run bandit -r api --skip B101,B105`
- **Allure results:** `uv run pytest --alluredir=allure-results`
- **Allure report (CLI):** `allure serve allure-results`

---

## License
MIT
