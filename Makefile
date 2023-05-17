.PHONY: format lint

format:
	black ./wander
	ruff --select I --fix ./wander

lint:
	black ./wander --check
	ruff ./wander