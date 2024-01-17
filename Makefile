
.PHONY: setup
setup:
	@echo "Setting up...."
	@python3 -m venv venv
	@(. venv/bin/activate && pip install hl7apy)

.PHONY run:
run:
	@echo "Running...."
	@(. venv/bin/activate && python3 hl7.py)