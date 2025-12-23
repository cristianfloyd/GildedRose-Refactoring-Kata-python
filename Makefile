.PHONY: install test coverage lint format clean

install:
	pip install -r requirements.txt

test:
	pytest -v

coverage:
	pytest --cov=gilded_rose --cov-report=html --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

run:
	python texttest_fixture.py
