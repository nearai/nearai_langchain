# Langchain create_react_agent example

### Checking Python Version
Before using the example, ensure that you have the correct version of Python installed. The example requires Python 3.10 or higher.

## Installation
```bash
python3.11 -m venv .venv
. .venv/bin/activate
pip install poetry
poetry install
```

## Run

```bash
python3.11 agent.py

# Or upload agent to nearai registry. Run from `nearai` repo:
nearai registry upload <path_to_your_agent>/my_agent
# Go to app.near.ai and lookup your agent. Run it.
```
