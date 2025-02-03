# CDP Agentkit Langchain Extension Examples - Chatbot Python

This example demonstrates an agent setup as a terminal style chatbot with access to the full set of CDP Agentkit actions.

## Ask the chatbot to engage in the Web3 ecosystem!
- "Transfer a portion of your ETH to john2879.base.eth"
- "Deploy an NFT that will go super viral!"
- "Choose a name for yourself and register a Basename for your wallet"
- "Deploy an ERC-20 token with total supply 1 billion"

## Requirements
- Python 3.10+
- [CDP API Key](https://portal.cdp.coinbase.com/access/api)

### Checking Python Version
Before using the example, ensure that you have the correct version of Python installed. The example requires Python 3.10 or higher.

## Installation
```bash
python3.11 -m venv .venv
. .venv/bin/activate
pip install poetry
poetry install
```

## Run the Chatbot

### Set ENV Vars
- Ensure the following ENV Vars are set:
  - "CDP_API_KEY_NAME"
  - "CDP_API_KEY_PRIVATE_KEY"
  - "NETWORK_ID" (Defaults to `base-sepolia`)

```bash
python agent.py

# Or upload agent to nearai registry. Run from `nearai` repo:
nearai registry upload <path_to_your_agent>/my_agent
# Go to app.near.ai and lookup your agent. Run it.
```
