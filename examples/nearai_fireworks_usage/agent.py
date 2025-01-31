"""Example usage of NearAI LangChain integration."""

from langchain_core.messages import HumanMessage, SystemMessage

from nearai_langchain.orchestrator import NearAILangchainOrchestrator

model = NearAILangchainOrchestrator(globals())

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]

print(model.invoke(messages))
