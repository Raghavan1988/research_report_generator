# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- `.gitignore` for Python artifacts, virtual environments, `.env`, and generated reports.
- `/health` endpoint for readiness checks.
- `/version` endpoint exposing the app name and version.
- `gunicorn` dependency for production serving.
- `.gitattributes` to normalize line endings.
- `CONTRIBUTING.md` with contribution guidelines.
- `Makefile` with common developer commands, including a `test` target.
- Test suite covering the health, version, and error routes.
- Module docstring describing the application.
- Table of contents in the README.
- API endpoints documentation in the README.
- Docker healthcheck against the `/health` endpoint.
- Non-root user in the Docker image.
- Loading state and client-side error handling on the report form.
- Responsive styling and mobile viewport for the web interface.
- "Running tests" instructions in `CONTRIBUTING.md`.
- JSON error handler for `500` responses.
- Request body size limit of 1 MB.

### Changed
- Report generation now returns a `502` response when upstream services fail.
- Topic input is now required and includes a placeholder hint.
- YOU.com API key is now read from the `YOU_COM_API_KEY` environment variable.
- Server port is now configurable via the `PORT` environment variable.
- OpenAI model is now configurable via the `OPENAI_MODEL` environment variable.
- Fixed the clone URL in the README to point to the actual repository.
- Search requests now use a timeout and no longer duplicate the query parameter.
- Replaced `print` statements with structured logging.
- Pinned `openai` to the `>=1.0.0` line to match the client API in use.
- Ignore common editor and OS artifacts (`.vscode/`, `.idea/`, `.DS_Store`, `*.swp`).

### Fixed
- Missing search queries no longer raise a `KeyError`.
- Report filenames are sanitized to prevent path traversal and invalid names.
