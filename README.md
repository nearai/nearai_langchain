# NearAI LangChain Integration

`nearai_langchain` provides seamless integration between [NearAI](https://github.com/nearai/nearai) and [LangChain](https://github.com/langchain-ai/langchain), allowing developers to use NearAI's capabilities within their LangChain applications.

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
              "model": "qwen2p5-72b-instruct",
              // Optionally, specify "model_provider". fireworks is used by default in nearai.
              "inference_framework": "nearai"  // Use "langchain" or "nearai" for inference. Optional. Default is "nearai".
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
python3.11 agent.py

# Or upload agent to nearai registry. Run from `nearai` repo:
nearai registry upload <path_to_your_agent>/my_agent
# Go to app.near.ai and lookup your agent. Run it.
```

Example agent code:
```python
from langchain_core.messages import SystemMessage

from nearai_langchain.orchestrator import NearAILangchainOrchestrator, RunMode

orchestrator = NearAILangchainOrchestrator(globals())
# To continue conversation on existing thread in local mode:
# orchestrator = NearAILangchainOrchestrator(globals(), thread_id="thread_xxxxxx")

# Langchain chat model that can be passed to other LangChain & LangGraph libraries.
model = orchestrator.chat_model

# NEAR AI environment.
# In remote mode thread is assigned, user messages are given, and an agent is run at least once per user message.
# In local mode an agent is responsible to get and upload user messages.
env = orchestrator.env

if orchestrator.run_mode == RunMode.LOCAL:
    print("English -> Italian Translator")
    user_input = input("\nEnglish: ")
    env.add_user_message(user_input)

messages = [SystemMessage("Translate the following from English into Italian")] + env.list_messages()

result = model.invoke(messages)
print(result)
env.add_reply(result.content)
if orchestrator.run_mode == RunMode.LOCAL:
    print("-------------------")
    print(result.content)
    print("-------------------")

# Run once per user message.
env.mark_done()
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
   
