# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added
- `.gitignore` for Python artifacts, virtual environments, `.env`, and generated reports.
- `/health` endpoint for readiness checks.
- `gunicorn` dependency for production serving.

### Changed
- YOU.com API key is now read from the `YOU_COM_API_KEY` environment variable.
- Server port is now configurable via the `PORT` environment variable.
- Fixed the clone URL in the README to point to the actual repository.
