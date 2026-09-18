# Contributing

Thanks for your interest in improving the Research Report Generator!

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your API keys.

## Making changes

- Create a feature branch off `main`.
- Keep commits small and focused, with clear messages.
- Make sure the app still starts (`python app.py`) before opening a pull request.

## Running tests

Install the dependencies and run the test suite before opening a pull request:

```bash
make test
```

This runs the tests under `tests/` with `pytest`.

## Pull requests

- Describe what your change does and why.
- Link any related issues.
- Update the `CHANGELOG.md` under `[Unreleased]` when appropriate.
