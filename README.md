# NearAI LangChain Integration

`nearai_langchain` provides seamless integration between [NearAI](https://github.com/nearai/nearai) and [LangChain](https://github.com/langchain-ai/langchain), allowing developers to use NearAI's capabilities within their LangChain applications.

## 🚧 Development Status

This library is currently in active development.

## 🎯 Key Purposes

1. **Optional NearAI Inference Integration**
   - Access model inference through NearAI's optimized infrastructure
   - Maintain compatibility with standard LangChain for other use cases
   - Seamlessly switch between NearAI and LangChain inference

2. **NearAI Registry Integration**
   - Register and manage agents in the NearAI registry
   - Auto-generate or validate agent metadata
   - Example `metadata.json`:
     ```json
     {
       "category": "agent",
       "name": "example_agent",
       "namespace": "user.nearai",
       "tags": ["example"],
       "details": {
         "agent": {
           "defaults": {
             "model": "accounts/fireworks/models/llama-v3p1-70b-instruct"
           },
           "framework": "langchain"  // Use "langchain" or "nearai" for inference
         }
       }
     }
     ```

3. **Benchmarking and Evaluation**
   - Run popular or user owned benchmarks on agents
   - Optionally, upload evaluation results to [NearAI evaluation table](https://app.near.ai/evaluations)
   - Support for both NearAI and LangChain inference frameworks

## 🌟 Features

- Drop-in replacement for LangChain chat models
- Support for multiple model providers
- Flexible framework switching between LangChain and NearAI
- Type-safe interfaces

## 🚀 Quick Start

```python
import getpass
import os

import nearai_langchain
from langchain_core.messages import HumanMessage, SystemMessage
from nearai_langchain.langchain_fireworks import ChatFireworks

NearaiLangchain.init() # Reads metadata and inits either Langchain or NearAI. Supports "langchain" or "nearai" frameworks.

model = ChatFireworks()
# Alternatively to use provider from metadata: model = ChatProvider()

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

model.invoke(messages)
```

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

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
