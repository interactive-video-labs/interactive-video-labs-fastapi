# Developer Guide

This guide covers local setup, testing, and running the FastAPI adapter.

## Requirements

- Python 3.10 or newer
- Poetry
- Git

## Setup

Clone the repository and install its dependencies:

```bash
git clone https://github.com/interactive-video-labs/interactive-video-labs-fastapi.git
cd interactive-video-labs-fastapi
poetry install
```

The package depends on `interactive-video-labs-core` 0.2.0 or newer. If you are
developing against an unpublished core version, install the core package into
the Poetry environment from its repository before working on this wrapper.

## Run the API

Start the development server:

```bash
poetry run uvicorn interactive_video_labs_fastapi.main:app --reload
```

The default app uses `sqlite+aiosqlite:///./interactive_video.db` and creates
the core ORM tables when the application starts. To use a different database
URL, construct the app with `create_app(database_url)` in your own entry point.

## Run Tests

Run the complete test suite:

```bash
poetry run pytest
```

The API tests use FastAPI's `TestClient` and an in-memory SQLite database.

## GitHub Actions

The workflows in `.github/workflows/` provide:

- `test.yml`: runs the test suite on pushes and pull requests targeting `main`
  using Python 3.10 through 3.13.
- `release.yml`: creates a GitHub Release when a `v*.*.*` tag is pushed.
- `publish.yml`: tests and builds the package, then publishes it to PyPI when a
  release is published. Configure PyPI trusted publishing for this repository
  with the `pypi` environment. Manual dispatch also publishes the current
  project version.
- `renovate.yml`: runs Renovate weekly or on demand. Configure the repository
  secret `RENOVATE_TOKEN` with a token that can create dependency update PRs.

The package version in `pyproject.toml` must match the release tag after
removing its optional `v` prefix.

## Package Layout

```text
interactive_video_labs_fastapi/
├── app.py             # Application factory and lifespan
├── dependencies.py    # Request-scoped SQLAlchemy repository
├── main.py            # Default ASGI application
├── models.py          # Request and response models
└── routes.py          # API endpoint handlers
tests/
└── test_api.py
```

## Implementation Notes

- Keep business logic and persistence contracts in `interactive-video-labs-core`.
- Use `AbstractSessionRepository` when adding alternate storage integrations.
- Keep FastAPI-specific request handling and dependency wiring in this package.
- Create database migrations through the consuming application's migration
  tooling for production deployments; automatic table creation is intended for
  this simple default setup.
