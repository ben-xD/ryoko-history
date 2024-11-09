# Backend

## Setup

- Install pyenv (python manager) with `brew install pyenv`
- Install python: `pyenv install`
- [Install uv](https://github.com/astral-sh/uv) by running `curl -LsSf https://astral.sh/uv/install.sh | sh` on linux/macOS
- Set up virtual env and install python dependencies: `uv sync`
- Configure VScode to use that new python environment

## Usage

- to add new dependency: e.g. `uv add $package_name`. Note: if adding packages with `[]`, use quotes like `uv add "fastapi[standard]"`
- start backend: `./scripts/dev.sh`
- Visit http://localhost:8000/docs use the OpenAPI page
- The API is on http://localhost:8000/
