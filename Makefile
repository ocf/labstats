.PHONY: test
test:
	pre-commit run --all-files

.PHONY: install-hooks
install-hooks:
	pre-commit install -f --install-hooks
