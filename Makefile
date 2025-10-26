# Copyright (c) 2025 Mikheil Tabidze
.PHONY: run-app run-ruff run-mypy run-unit-testing run-functional-testing run-coverage-measurement run-static-code-analysis run-ci-pipeline

run-app:
	@echo "\nRunning the application ...\n"
	streamlit run app/src/streamlit_app.py

run-ruff:
	@echo "\nRunning Ruff lint and format ...\n"
	ruff format --config pyproject.toml app
	ruff check --fix --config pyproject.toml app/src


run-mypy:
	@echo "\nRunning mypy type check ...\n"
	mypy --config-file pyproject.toml app/src


run-unit-testing:
	@echo "\nUnit testing has begun\n"
	@UNIT_TESTING_EXIT_CODE=0; \
	coverage run \
	  --source=app/src --data-file=.cover/unit-testing/unit-testing.coverage --module \
	  pytest --verbose --random-order app/tests/unit_tests || UNIT_TESTING_EXIT_CODE=$$?; \
	coverage html \
	  --data-file=.cover/unit-testing/unit-testing.coverage --directory=.cover/unit-testing/html; \
	echo -e "\nUnit testing has completed with exit code $$UNIT_TESTING_EXIT_CODE\n"; \
	if [ $$UNIT_TESTING_EXIT_CODE -ne 0 ]; then \
	  exit 1; \
	fi


run-functional-testing:
	@echo "\nFunctional testing has begun\n"
	@FUNCTIONAL_TESTING_EXIT_CODE=0; \
	coverage run \
	  --source=app/src --data-file=.cover/functional-testing/functional-testing.coverage --module \
	  pytest --verbose --random-order app/tests/functional_tests || FUNCTIONAL_TESTING_EXIT_CODE=$$?; \
	coverage html \
	  --data-file=.cover/functional-testing/functional-testing.coverage --directory=.cover/functional-testing/html; \
	echo -e "\nFunctional testing has completed with exit code $$FUNCTIONAL_TESTING_EXIT_CODE\n"; \
	if [ $$FUNCTIONAL_TESTING_EXIT_CODE -ne 0 ]; then \
	  exit 1; \
	fi


run-coverage-measurement:
	@echo "\nCoverage measurement has begun\n"
	@UNIT_TESTING_COVERAGE_EXIT_CODE=0; \
	FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE=0; \
	coverage report --data-file=.cover/unit-testing/unit-testing.coverage --fail-under=75 || UNIT_TESTING_COVERAGE_EXIT_CODE=$$?; \
	coverage report --data-file=.cover/functional-testing/functional-testing.coverage --fail-under=75 || FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE=$$?; \
	echo -e "\nCoverage measurement has completed with the following results:\n\n  1. Unit testing coverage exit code - $$UNIT_TESTING_COVERAGE_EXIT_CODE\n  2. Functional testing coverage exit code - $$FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE\n"; \
	COVERAGE_MEASUREMENT_RESULT=$$(( $$UNIT_TESTING_COVERAGE_EXIT_CODE + $$FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE )); \
	if [ $$COVERAGE_MEASUREMENT_RESULT -ne 0 ]; then \
	  exit 1; \
	fi


run-static-code-analysis:
	@echo "\nStatic code analysis has begun\n"
	@RUFF_LINTER_EXIT_CODE=0; \
	RUFF_FORMATTER_EXIT_CODE=0; \
	MYPY_EXIT_CODE=0; \
	PIP_LICENSES_EXIT_CODE=0; \
	PIP_AUDIT_EXIT_CODE=0; \
	ruff check --config pyproject.toml app/src || RUFF_LINTER_EXIT_CODE=$$?; \
	ruff format --check --config pyproject.toml app/src || RUFF_FORMATTER_EXIT_CODE=$$?; \
	mypy --config-file pyproject.toml app/src || MYPY_EXIT_CODE=$$?; \
	pip-licenses --order=license --fail-on="GPL;GPLv2;GPLv3;LGPL;LGPLv2.1;LGPLv3" || PIP_LICENSES_EXIT_CODE=$$?; \
	pip-audit || PIP_AUDIT_EXIT_CODE=$$?; \
	echo -e "\nStatic code analysis has completed with the following results:\n\n  1. Ruff Linter exit code - $$RUFF_LINTER_EXIT_CODE\n  2. Ruff Formatter exit code - $$RUFF_FORMATTER_EXIT_CODE\n  3. Mypy exit code - $$MYPY_EXIT_CODE\n  4. pip-licenses exit code - $$PIP_LICENSES_EXIT_CODE\n  5. pip-audit exit code - $$PIP_AUDIT_EXIT_CODE\n"; \
	STATIC_CODE_ANALYSIS_RESULT=$$(( $$RUFF_LINTER_EXIT_CODE + $$RUFF_FORMATTER_EXIT_CODE + $$MYPY_EXIT_CODE + $$PIP_LICENSES_EXIT_CODE + $$PIP_AUDIT_EXIT_CODE )); \
	if [ $$STATIC_CODE_ANALYSIS_RESULT -ne 0 ]; then \
	  exit 1; \
	fi


run-ci-pipeline:
	@echo "\nTesting has begun\n"
	@UNIT_TESTING_EXIT_CODE=0; \
	FUNCTIONAL_TESTING_EXIT_CODE=0; \
	COVERAGE_MEASUREMENT_EXIT_CODE=0; \
	STATIC_CODE_ANALYSIS_EXIT_CODE=0; \
	$(MAKE) --no-print-directory run-unit-testing || UNIT_TESTING_EXIT_CODE=$$?; \
	$(MAKE) --no-print-directory run-functional-testing || FUNCTIONAL_TESTING_EXIT_CODE=$$?; \
	$(MAKE) --no-print-directory run-coverage-measurement || COVERAGE_MEASUREMENT_EXIT_CODE=$$?; \
	$(MAKE) --no-print-directory run-static-code-analysis || STATIC_CODE_ANALYSIS_EXIT_CODE=$$?; \
	echo -e "\nTesting has completed with the following results:\n\n  1. Unit testing exit code - $$UNIT_TESTING_EXIT_CODE\n  2. Functional testing exit code - $$FUNCTIONAL_TESTING_EXIT_CODE\n  3. Coverage measurement exit code - $$COVERAGE_MEASUREMENT_EXIT_CODE\n  4. Static code analysis exit code - $$STATIC_CODE_ANALYSIS_EXIT_CODE\n"; \
	TESTS_RESULT=$$(( $$UNIT_TESTING_EXIT_CODE + $$FUNCTIONAL_TESTING_EXIT_CODE + $$COVERAGE_MEASUREMENT_EXIT_CODE + $$STATIC_CODE_ANALYSIS_EXIT_CODE )); \
	if [ $$TESTS_RESULT -ne 0 ]; then \
	  exit 1; \
	fi
