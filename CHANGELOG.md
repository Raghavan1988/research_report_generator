# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- `.gitignore` for Python artifacts, virtual environments, `.env`, and generated reports.
- `/health` endpoint for readiness checks.
- `gunicorn` dependency for production serving.
- `.gitattributes` to normalize line endings.
- `CONTRIBUTING.md` with contribution guidelines.
- `Makefile` with common developer commands.
- JSON error handler for `500` responses.
- Request body size limit of 1 MB.

### Changed
- YOU.com API key is now read from the `YOU_COM_API_KEY` environment variable.
- Server port is now configurable via the `PORT` environment variable.
- Fixed the clone URL in the README to point to the actual repository.
- Search requests now use a timeout and no longer duplicate the query parameter.
- Replaced `print` statements with structured logging.

### Fixed
- Missing search queries no longer raise a `KeyError`.
- Report filenames are sanitized to prevent path traversal and invalid names.
