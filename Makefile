.PHONY: test, fix, lint, lint-fix

test:
	pytest --cov

test-watch:
	ptw tacview_timesync/ tests/ -- tests/ --cov

lint:
	flake8 --statistics --tee

fix:
	black .
	autoflake -r --in-place --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports --remove-duplicate-keys .

lint-fix: fix lint