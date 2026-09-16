.PHONY: install run prod clean

install:
	pip install -r requirements.txt

run:
	python app.py

prod:
	gunicorn app:app --bind 0.0.0.0:$${PORT:-5000}

clean:
	rm -f static/report_*.html
	find . -type d -name __pycache__ -exec rm -rf {} +
