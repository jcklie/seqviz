format:
	black -l 120 seqviz/
	black -l 120 tests/

	isort .

test:
	python -m pytest tests/
