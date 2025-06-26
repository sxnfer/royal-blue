# Royal Blue

## Table of Contents
1. [Introduction](#introduction)  
2. [Project Description](#project-description)  
3. [Requirements](#requirements)  
4. [Installation Instructions](#installation-instructions)  
5. [Running Python Scripts Locally](#running-python-scripts-locally)  
6. [Makefile Commands](#makefile-commands)  

---

## Introduction

**Royal Blue** is an Extract, Load, Transform (ETL) data pipeline built on top of AWS using Python, Terraform and Pandas.

It was built as a graduation project for the [Northcoders](https://www.northcoders.com) Data Engineering in Python bootcamp that ran from March to June 2025.

---

## Project Description

The purpose of this repository is to build an entire ETL (Extract, Load, Transform) data pipeline in AWS (Amazon Web Services).

It implements a robust and scalable solution for extracting, transforming, and loading data from an OLTP (Online Transaction Processing) PostgreSQL database and loading it into an OLAP (Online Analytical Processing) database.

Follow these links for the [origin](https://dbdiagram.io/d/6332fecf7b3d2034ffcaaa92) and [destination](https://dbdiagram.io/d/63a19c5399cb1f3b55a27eca) database Entity Relationship Diagrams.

The data is transformed from transactional day-to-day business data into a Data Analysis-ready format, suitable for multiple Business intelligence purposes.

It uses [Python](https://www.python.org) as the main programming language, followed by [Terraform](https://www.hashicorp.com/en/products/terraform) for infrastructure as code. It also uses Bash and SQL Scripts to help with build processes and integration testing, and has a full-featured Makefile for convenience.
    
This project follows the specs proposed for the [Northcoders Data Engineering graduation project](https://github.com/northcoders/de-project-specification/blob/main/README.md) and was developed as a group effort by [@theorib](https://github.com/theorib), [@Brxzee](https://github.com/Brxzee), [@charleybolton](https://github.com/charleybolton), [@JanetteSamuels](https://github.com/JanetteSamuels), [@sxnfer](https://github.com/sxnfer) and [@josephtheodore](https://github.com/josephtheodore).

---

## Requirements

- This project uses [uv](https://docs.astral.sh/uv/) to manage Python environments, dependencies, running scripts, and for our build process. Make sure it is installed by following the [official guide](https://docs.astral.sh/uv/getting-started/installation/).

- You will also need to install the [latest version of Python](https://www.python.org/downloads/) (3.13.3 at the time of this writing).

- For local development, you will need the [AWS CLI](https://aws.amazon.com/cli/) installed and configured with your AWS credentials.

- To run some of the integration tests, you will need to [install PostgreSQL locally](https://www.postgresql.org/download/) v14 or higher. 

---

## Tech Stack

**Programming Language & Runtime**  
- Python 3.13.3+  

**Core Python Dependencies**  
- [Psycopg 3](https://www.psycopg.org/psycopg3/docs/) - PostgreSQL database adapter
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - for AWS SDK integration
- [pandas](https://pandas.pydata.org/docs/) - for data manipulation
- [PyArrow](https://arrow.apache.org/docs/python/) - for Parquet file handling
- [Pydantic](https://docs.pydantic.dev/latest/) - for data validation and JSON serialisation

**Development Dependencies**  
- [pytest](https://docs.pytest.org/en/stable/) - and related plugins for testing and coverage  
- [pytest-postgresql](https://github.com/dbfixtures/pytest-postgresql) - using for running integration tests against local PostgreSQL databases  
- [Ruff](https://docs.astral.sh/ruff/) - for linting and formatting
- [Moto](https://docs.getmoto.org/en/latest/docs/getting_started.html) - for mocking AWS services during tests
- [Bandit](https://bandit.readthedocs.io/en/latest/) - for vulnerability and security scanning of source code
- [IPython Kernel](https://ipykernel.readthedocs.io/en/stable/) - for VS Code Jupyter notebook support, used for testing and experimenting

**Databases**  
- [PostgreSQL](https://www.postgresql.org) (used locally for integration tests, as well as being the database used on both sides of the data pipeline).

**AWS**  
- Lambda, S3, Step Functions, IAM, Cloudwatch, SNS Email alerts, etc. All accessed using [`boto3`](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) deployed with [Terraform](https://www.hashicorp.com/en/products/terraform) and tested using Moto.

**Utilities & Tooling**  
- [`uv`](https://docs.astral.sh/uv/) for managing Python environments, dependencies, and running scripts
- `Makefile` for convenience, centralising and simplifying the project’s most common commands (testing, linting, formatting, deployment, etc).

**Local Testing Scripts**  
- Bash scripts to run SQL test files against the local PostgreSQL database and capture output for validation.

---

## Installation Instructions

1. Clone or fork this repository and download it to your local machine:

    ```bash
    git clone https://github.com/theorib/royal-blue.git
    ```

2. Change directory into the cloned repository:

    ```bash
    cd royal-blue
    ```

3. Create a `.env` file at the root, based on the `.env.example` provided. Ensure essential variables like those starting with `DB_` are set. Others, like S3 bucket names, are only needed if you plan to run scripts locally.

    ```bash
    TOTESYS_DB_USER=some_user_abc
    TOTESYS_DB_PASSWORD=some_password_xyz
    TOTESYS_DB_HOST=host.something.com
    TOTESYS_DB_DATABASE=database_name
    TOTESYS_DB_PORT=0000
    DATAWAREHOUSE_DB_USER=some_user_abc
    DATAWAREHOUSE_DB_PASSWORD=some_password_xyz
    DATAWAREHOUSE_DB_HOST=host.something.com
    DATAWAREHOUSE_DB_DATABASE=database_name
    DATAWAREHOUSE_DB_PORT=0000
    
    # For local integration tests only:
    INGEST_ZONE_BUCKET_NAME=some_bucket_name
    PROCESS_ZONE_BUCKET_NAME=some_bucket_name
    LAMBDA_STATE_BUCKET_NAME=another_bucket_name
    ```

4. If you forked this repository and want CI/CD to work as intended, you will have to create GitHub Secrets for the above environment variables (except for the local integration ones). 

5. Run the setup script (this will install dependencies, run tests and checks):

    ```bash
    make setup
    ```

---

## Running Python Scripts Locally

With `uv` managing the environment, running your scripts is clean and consistent. Here's how to start:


1. Activate the Python virtual environment:

    ```bash
    source .venv/bin/activate
    ```

2. Set the `PYTHONPATH` environment variable to the current directory:

    ```bash
    export PYTHONPATH=$(pwd)
    ```

3. Point `uv` to your local `.env` file so that environment variables are available to running scripts:

    ```bash
    export UV_ENV_FILE=.env
    ```

4. Run Python scripts or tests using `uv run`:

    ```bash
    uv run src/lambdas/extract_lambda.py
    ```

    Example on how to run tests:

    ```bash
    uv run pytest
    ```

---

## Available Makefile Commands

Use these main commands for common tasks:

| Command               | Description                                         |
|-----------------------|-----------------------------------------------------|
| `make setup`          | Complete installation and validation (sync, build, checks) |
| `make test`           | Run all tests                                      |
| `make fix`            | Run formatter and linter                            |
| `make safe`           | Run security scans                                 |
| `make help`           | Show all available make commands                    |

For a full list of commands and their description, run:

```bash
make help
```

