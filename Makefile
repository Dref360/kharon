.PHONY: lint
lint: check-mypy-error-count
	poetry run flake8 kharon service

.PHONY: test
test: lint
	poetry run pytest tests --cov=kharon

.PHONY: format
format:
	poetry run black kharon service

.PHONY: mypy
mypy:
	poetry run mypy --implicit-reexport --show-error-codes kharon service


.PHONY: check-mypy-error-count
check-mypy-error-count: MYPY_INFO = $(shell expr `poetry run mypy kharon | grep ": error" | wc -l`)
check-mypy-error-count: MYPY_ERROR_COUNT = 0

check-mypy-error-count:
	@if [ ${MYPY_INFO} -gt ${MYPY_ERROR_COUNT} ]; then \
		echo mypy error count $(MYPY_INFO) is more than $(MYPY_ERROR_COUNT); \
		false; \
	fi

SRC_FOLDER    ?= ./kharon ./service
REPORT_FOLDER ?= ./reports

./reports/security/bandit/:
		@mkdir -p ./reports/security/bandit/

.PHONY: bandit
bandit: ./reports/security/bandit/ ## SECURITY - Run bandit
		poetry run bandit ${SRC_FOLDER}/* -r -x "*.pyi,*/_generated/*,*__pycache__*" -v -ll -f json > ${REPORT_FOLDER}/security/bandit/index.json

.PHONY: build
build: build_fe build_be build_service

.PHONY: build_be
build_be:
	docker build -t dref360/kharon-backend .

.PHONY: build_fe
build_fe:
	docker build -t dref360/kharon-frontend webapp

.PHONY: build_service
build_service:
	docker build -t dref360/kharon-service service

.PHONY: push
push: push_fe push_be push_service

.PHONY: build_be
push_be:
	docker push dref360/kharon-backend

.PHONY: build_fe
push_fe:
	docker push dref360/kharon-frontend

.PHONY: build_service
push_service:
	docker push dref360/kharon-service