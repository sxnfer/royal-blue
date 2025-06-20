##@ Utility
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

.PHONY: uv
uv:  ## Install uv if it's not present
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	
.PHONY: sync
sync: uv ## Install dependencies
	uv sync

.PHONY: test
test:  ## Run tests
	uv run pytest

.PHONY: lint
lint:  ## Run Ruff linter
	uv run ruff check ./src ./tests --fix

.PHONY: fmt
fmt:  ## Run Ruff formatter
	uv run ruff format --verbose ./src ./tests

.PHONY: fmt-tf
fmt-tf: ## Run Terraform formatter
	@cd terraform && terraform init && terraform fmt -recursive

.PHONY: fix
fix:  fmt lint ## Run Ruff linter and formatter

.PHONY: fix-all 
fix-all:  fmt lint fmt-tf ## Run Ruff linter, formatter and Terraform formatter

.PHONY: cov
cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term-missing

.PHONY: safe
safe: ## Run Bandit security scan
	uv run bandit -r -lll src

.PHONY: checks
checks: fix-all cov safe ## Run all checks

.PHONY: set-tfvars
set-tfvars:  ## Copy .env variables to terraform/terraform.auto.tfvars file
	./set-tfvars.sh

.PHONY: run-tf-build-scripts
run-tf-build-scripts:  ## Run all build scripts necessary to run terraform plan and apply
	./build_lambda_layer.sh && ./build_extract_lambda_zip.sh && ./build_transform_lambda_zip.sh && ./build_load_lambda_zip.sh

.PHONY: run-sql-files
run-sql-files:  ## Run all SQL files in the sql directory
	./sh_scripts/run_sql_files.sh 

.PHONY: setup
setup: sync run-tf-build-scripts set-tfvars checks ## Runs all checks and instalation scripts to get your project running
