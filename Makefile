.PHONY: install run prod test clean

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m pytest -q

prod:
	gunicorn app:app --bind 0.0.0.0:$${PORT:-5000}

clean:
	rm -f static/report_*.html
	find . -type d -name __pycache__ -exec rm -rf {} +
