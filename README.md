# NearAI LangChain Integration

`nearai_langchain` provides seamless integration between NearAI and LangChain, allowing developers to use NearAI's capabilities within their LangChain applications.

## 🚧 Development Status

This library is currently in active development.

## 🌟 Features

- Drop-in replacement for LangChain chat models
- Support for multiple model providers
- Flexible framework switching between LangChain and NearAI
- Type-safe interfaces

## 🚀 Quick Start

```python
from nearai_langchain import NearAILangchain
from nearai_langchain.chat_models.providers.fireworks import ChatFireworks

# Initialize with NearAI framework
NearAILangchain.init(framework="nearai")

# Create chat model
model = ChatFireworks()

# Use just like a regular LangChain chat model
response = model.generate([
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="Hello!")
])
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
