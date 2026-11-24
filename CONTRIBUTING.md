# Contributing

Thank you for your interest in contributing to `interactive-video-labs-fastapi`.

We welcome focused improvements to the FastAPI adapter, request handling,
dependency wiring, tests, documentation, and developer tooling. Contributions
should be compatible with Python 3.10 and newer.

Please open an issue before starting a large feature or public API change.

---

## Ways to Contribute

- Report bugs or unexpected API behavior.
- Improve FastAPI routes, application setup, or dependency handling.
- Add or improve tests and documentation.
- Improve framework integration for `interactive-video-labs-core`.
- Fix typing, packaging, or dependency issues.

Core decision logic, models, and storage contracts belong in
[`interactive-video-labs-core`](https://github.com/interactive-video-labs/interactive-video-labs-core).
This repository should remain focused on the FastAPI adapter. The core live
protocol is framework-independent; WebSocket connection management belongs in
the consuming application.

---

## Development Setup

### Prerequisites

- Python 3.10 or newer
- Poetry
- Git

### Clone the Repository and Install Dependencies

```bash
git clone https://github.com/interactive-video-labs/interactive-video-labs-fastapi.git
cd interactive-video-labs-fastapi
poetry install
```

The package depends on `interactive-video-labs-core` 0.3.0 or newer. If you are
developing against an unpublished core version, install that version into the
Poetry environment before working on this adapter.

Prefix project commands with `poetry run`, or use the Poetry environment
directly.

---

## Project Structure

```text
interactive-video-labs-fastapi/
├── interactive_video_labs_fastapi/
│   ├── app.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── tests/
│   └── test_api.py
├── pyproject.toml
├── README.md
└── DEVELOPER.md
```

### Core Modules

- `app.py` creates the FastAPI application and manages its lifespan.
- `dependencies.py` provides request-scoped database/repository dependencies.
- `main.py` exposes the default ASGI application.
- `models.py` contains adapter-specific request and response models.
- `routes.py` contains the HTTP endpoint handlers.

Keep FastAPI-specific request handling and dependency wiring in this package.
Use `interactive-video-labs-core` for shared decision logic and persistence
contracts.

---

## Making Changes

1. Create a focused branch from the latest default branch.
2. Make the smallest complete change that solves the problem.
3. Follow existing naming, typing, and code organization conventions.
4. Add or update tests for behavior changes.
5. Run the relevant tests and build checks.
6. Update documentation when public behavior or setup changes.

Use descriptive branch names, such as:

```text
fix/session-resume-response
feature/transition-endpoint
docs/improve-setup-guide
test/api-error-cases
```

---

## Running Tests and Build Checks

Run the complete test suite:

```bash
poetry run pytest
```

The API tests use FastAPI's `TestClient` and an in-memory SQLite database.
Keep tests isolated and include coverage for new public behavior and relevant
validation or error paths.

Build the package distributions with:

```bash
poetry build
```

The GitHub Actions test workflow runs the test suite on Python 3.10 through
3.13.

---

## Code and API Guidelines

- Keep changes focused on the FastAPI adapter.
- Preserve the public API and existing response behavior unless a change is
  intentional and documented.
- Add type hints to public interfaces and follow existing project patterns.
- Use the existing Pydantic and SQLAlchemy dependencies rather than introducing
  unnecessary abstractions or dependencies.
- Keep database sessions request-scoped through the existing dependency
  patterns.
- Use the consuming application's migration tooling for production database
  schema changes; automatic table creation is intended for the default setup.
- Add tests for route behavior and adapter integration.

---

## Pull Requests

Pull requests should include:

- A clear summary of the change and why it is needed.
- Tests for new or modified behavior.
- Documentation updates when applicable.
- Compatibility or migration notes for changes affecting consumers.
- Links to related issues.

Before submitting, run:

```bash
poetry run pytest
poetry build
git diff --check
```

Keep pull requests focused and separate unrelated changes.

---

## Bug Reports

Please include:

- A clear description of the issue.
- Steps to reproduce it.
- Expected and actual behavior.
- Python and dependency versions.
- Relevant logs or stack traces.
- A minimal code example when possible.

Do not include credentials, private keys, personal data, or production database
contents in bug reports or test data.

---

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
