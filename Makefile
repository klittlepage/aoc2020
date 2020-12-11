.PHONY: format
format:
	autopep8 -i -r aoc tests

.PHONY: lint
lint:
	pylint aoc tests
	mypy aoc tests

.PHONY: test
test:
	python3 -m unittest discover
