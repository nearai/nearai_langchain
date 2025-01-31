# NearAI LangChain Integration

`nearai_langchain` provides seamless integration between [NearAI](https://github.com/nearai/nearai) and [LangChain](https://github.com/langchain-ai/langchain), allowing developers to use NearAI's capabilities within their LangChain applications.

## 🚧 Development Status

This library is currently in active development.

## 🎯 Key Purposes

1. **Libraries Support**
   - Langchain
   - Langgraph
   - Coinbase AgentKit

2. **Optional NearAI Inference Integration**
   - Access model inference through NearAI's optimized infrastructure
   - Maintain compatibility with standard LangChain for other use cases
   - Seamlessly switch between NearAI and LangChain inference

3. **NearAI Registry Integration**
   - Register and manage agents in the NearAI registry
   - Optionally, enable agent-to-agent interaction and make your agents callable by other agents in the NearAI registry
   - Auto-generate or validate agent metadata
   - Example `metadata.json`:
     ```json
     {
      "name": "langchain_fireworks_example_usage",
      "version": "0.0.1",
      "description": "NEAR AI - Langchain Fireworks example usage",
      "category": "agent",
      "tags": [],
      "details": {
         "agent": {
            "defaults": {
              "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
              // Optionally, specify "model_provider"
              "inference_framework": "langchain"  // Use "langchain" or "nearai" for inference
            },
            "framework": "agentkit"  // Used by nearai hub to assign correct dependencies
         }
      },
      "show_entry": true
     }

4. **Agent Intercommunication**
   - Upload agents to be used by other agents
   - Call other agents from the registry in your own agents
   - Framework-agnostic: works with both NearAI and LangChain inference

5. **Benchmarking and Evaluation**
   - Run popular or user owned benchmarks on agents
   - Optionally, upload evaluation results to [NearAI evaluation table](https://app.near.ai/evaluations)
   - Support for both NearAI and LangChain inference frameworks

## 🚀 Quick Start

Your agent code and `metadata.json` must be in the same directory. You must run your agent script from that directory:

```bash
# Directory structure:
my_agent/
  ├── metadata.json
  ├── agent.py
  └── [other files...]

# Navigate to agent directory
cd my_agent

# Run your agent locally
python agent.py

# Or upload agent to nearai registry
# Run in hub
```

Example agent code:
```python
from langchain_core.messages import HumanMessage, SystemMessage

from nearai_langchain.orchestrator import NearAILangchainOrchestrator

# Orchestrator will read metadata.json from current directory
model = NearAILangchainOrchestrator()

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

model.invoke(messages)
```

See `examples/` folder for more examples.

## 📦 Installation

```bash
pip install nearai-langchain
```

## 🛠️ Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/nearai/nearai_langchain.git
   cd nearai_langchain
   ```

2. Install dependencies:
   ```bash
   ./install.sh
   ```

3. Development tools:
- Run format check: `./scripts/format_check.sh`
- Run linting: `./scripts/lint_check.sh`
- Run type check: `./scripts/type_check.sh`
   