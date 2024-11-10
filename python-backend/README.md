# Backend

## Setup

- Install pyenv (python manager) with `brew install pyenv`
- Install python: `pyenv install`
- [Install uv](https://github.com/astral-sh/uv) by running `curl -LsSf https://astral.sh/uv/install.sh | sh` on linux/macOS
- Set up virtual env and install python dependencies: `uv sync`
- Configure VScode to use that new python environment
- Create cloudflare account and create an R2 bucket (remember the name)
- Install [mypy VScode extension](https://marketplace.visualstudio.com/items?itemName=matangover.mypy)
- Optional: Install `AWS boto3` vscode extension
  - Warning: don't install Pylance, because it [breaks intellisense in vscode](https://stackoverflow.com/questions/50389852/visual-studio-code-intellisense-not-working). If you did that, uninstall Pylance extension, and uninstall python extension, and install Python extension again.

## Usage

- to add new dependency: e.g. `uv add $package_name`. Note: if adding packages with `[]`, use quotes like `uv add "fastapi[standard]"`
- start backend: `./scripts/dev.sh`
- Visit http://localhost:8000/docs use the OpenAPI page
- The API is on http://localhost:8000/


## TODOs

- Wait for AI video to be generated and download them, stitch them together with ffmpeg
- Use ElevenLabs conversational AI to get chat
