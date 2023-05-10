.PHONY: format lint

format:
	black .
	ruff --select I --fix .

lint:
	black . --check
	ruff .