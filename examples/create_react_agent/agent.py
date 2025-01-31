from langgraph.prebuilt import create_react_agent

from nearai_langchain.orchestrator import NearAILangchainOrchestrator, RunMode

orchestrator = NearAILangchainOrchestrator(globals())
# To continue conversation in local mode:
# orchestrator = NearAILangchainOrchestrator(globals(), thread_id="thread_xxxxxx")


def initialize_agent():
    """Initialize the agent."""
    # Initialize LLM.
    llm = orchestrator.chat_model

    # Create ReAct Agent using the LLM and no tools.
    return create_react_agent(
        llm,
        tools=[],
        state_modifier=("You are a helpful agent. Your name is CreateReactAgentExample."),
    )


executor = initialize_agent()
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

env.mark_done()
