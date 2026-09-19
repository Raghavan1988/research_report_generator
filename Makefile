.PHONY: help install run prod test clean freeze

help:
	@echo "Available targets:"
	@echo "  install  Install dependencies from requirements.txt"
	@echo "  run      Run the development server"
	@echo "  prod     Run the production server with gunicorn"
	@echo "  test     Run the test suite"
	@echo "  freeze   Write installed package versions to requirements.lock"
	@echo "  clean    Remove generated reports and caches"

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.lock

run:
	python app.py

test:
	python -m pytest -q

prod:
	gunicorn app:app --bind 0.0.0.0:$${PORT:-5000}

clean:
	rm -f static/report_*.html
	find . -type d -name __pycache__ -exec rm -rf {} +
