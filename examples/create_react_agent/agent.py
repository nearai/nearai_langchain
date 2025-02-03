from langgraph.prebuilt import create_react_agent

from nearai_langchain.orchestrator import NearAILangchainOrchestrator, RunMode

orchestrator = NearAILangchainOrchestrator(globals())
# To continue conversation on existing thread in local mode:
# orchestrator = NearAILangchainOrchestrator(globals(), thread_id="thread_xxxxxx")


def initialize_agent():
    """Initialize the agent."""
    # Get ChatOpenAI model.
    llm = orchestrator.chat_model.chat_open_ai_model

    # Create ReAct Agent using the LLM and no tools.
    return create_react_agent(
        llm,
        tools=[],
        state_modifier=("You are a helpful agent. Your name is CreateReactAgentExample."),
    )


executor = initialize_agent()

# NEAR AI environment.
# In remote mode thread is assigned, user messages are given, and an agent is run at least once per user message.
# In local mode an agent is responsible to get and upload user messages.
env = orchestrator.env

if orchestrator.run_mode == RunMode.LOCAL:
    print("Entering chat mode...")
    user_input = input("\nPrompt: ")
    env.add_user_message(user_input)

messages = env.list_messages()
for chunk in executor.stream({"messages": messages}):
    if "agent" in chunk:
        result = chunk["agent"]["messages"][0].content
    elif "tools" in chunk:
        result = chunk["tools"]["messages"][0].content
    env.add_reply(result)

    if orchestrator.run_mode == RunMode.LOCAL:
        print(result)
        print("-------------------")

# Run once per user message.
env.mark_done()
