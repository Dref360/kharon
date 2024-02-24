.PHONY: lint
lint: check-mypy-error-count
	poetry run flake8 shared_science

.PHONY: test
test: lint
	poetry run pytest tests --cov=shared_science

.PHONY: format
format:
	poetry run black shared_science

.PHONY: mypy
mypy:
	poetry run mypy --show-error-codes shared_science


.PHONY: check-mypy-error-count
check-mypy-error-count: MYPY_INFO = $(shell expr `poetry run mypy shared_science | grep ": error" | wc -l`)
check-mypy-error-count: MYPY_ERROR_COUNT = 0

check-mypy-error-count:
	@if [ ${MYPY_INFO} -gt ${MYPY_ERROR_COUNT} ]; then \
		echo mypy error count $(MYPY_INFO) is more than $(MYPY_ERROR_COUNT); \
		false; \
	fi

SRC_FOLDER    ?= ./shared_science
REPORT_FOLDER ?= ./reports

./reports/security/bandit/:
		@mkdir -p ./reports/security/bandit/

.PHONY: bandit
bandit: ./reports/security/bandit/ ## SECURITY - Run bandit
		poetry run bandit ${SRC_FOLDER}/* -r -x "*.pyi,*/_generated/*,*__pycache__*" -v -ll -f json > ${REPORT_FOLDER}/security/bandit/index.json

