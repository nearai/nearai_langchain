import getpass
import json
import os
from enum import Enum
from typing import Any, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_fireworks import ChatFireworks
from langchain_openai import ChatOpenAI
from nearai.agents.environment import Environment  # type: ignore
from nearai.openapi_client import EntryMetadataInput

from nearai_langchain.agent_data import NearAIAgentData
from nearai_langchain.constants import FIREWORKS, HYPERBOLIC
from nearai_langchain.local_environment import LocalEnvironment
from nearai_langchain.nearai_chat_model import NearAIChatModel


class RunMode(Enum):
    """Enum for different run modes of the orchestrator.

    In remote mode thread is assigned, user messages are given, and an agent is run at least once per user message.
    In local mode an agent is responsible to get and upload user messages.
    """

    LOCAL = "local"
    REMOTE = "remote"


class NearAILangchainOrchestrator:
    """Orchestrates chat model inference while tracking conversation history in NEAR AI."""

    chat_model: BaseChatModel | NearAIChatModel
    run_mode: RunMode
    env: Environment | LocalEnvironment

    def __init__(
        self,
        chat_model: Optional[BaseChatModel | NearAIChatModel] = None,
        skip_inference_framework_check: bool = False,
        thread_id: str = "",
    ):
        """Initialize the orchestrator with a chat model and metadata.

        Args:
        ----
            chat_model: Optional chat model to use. Can be either a LangChain chat model or NearAIChatModel.
                LangChain chat model may use any provider.
                If not provided, will create one based on metadata; fireworks and hyperbolic providers are supported.
            skip_inference_framework_check: If True, skips validation that the provided chat model matches
                the inference framework specified in metadata. This is useful when deliberately mixing
                inference frameworks, while still wanting to track all conversations in NEAR AI.
            thread_id: Optional thread ID for tracking conversation history in local mode.

        Raises:
        ------
            ValueError: If inference framework check fails or if metadata is invalid.
            FileNotFoundError: If metadata.json is not found.

        """
        self.run_mode = self._determine_run_mode()

        metadata_path = "metadata.json"
        with open(metadata_path, "r") as file:
            metadata = json.load(file)
        EntryMetadataInput.model_validate(metadata)
        agent_data = NearAIAgentData(metadata)

        # Initialize environment
        if self.run_mode == RunMode.REMOTE:
            self.env = globals()["env"]
        else:
            self.env = LocalEnvironment(thread_id, agent_data.agent_id)

        inference_framework = agent_data.inference_framework

        if inference_framework != "nearai" and inference_framework != "langchain":
            raise ValueError(f"Unsupported inference framework {inference_framework}.")

        if chat_model is None:
            if inference_framework == "nearai":
                self.chat_model = NearAIChatModel(agent_data=agent_data)
            else:
                self.chat_model = _init_langchain_chat_model(agent_data.provider, agent_data.metadata_model)
        else:
            if not skip_inference_framework_check:
                if inference_framework == "nearai" and not isinstance(chat_model, NearAIChatModel):
                    raise ValueError("Metadata specifies nearai framework but received non-NearAI chat model")
                if inference_framework == "langchain" and isinstance(chat_model, NearAIChatModel):
                    raise ValueError("Metadata specifies langchain framework but received NearAI chat model")
            self.chat_model = chat_model

    @staticmethod
    def _determine_run_mode() -> RunMode:
        """Determine the run mode based on the presence of env in globals."""
        return RunMode.REMOTE if "env" in globals() else RunMode.LOCAL

    def invoke(  # noqa: D102
        self,
        input: Any,
        **kwargs: Any,
    ) -> Any:
        return self.chat_model.invoke(input, **kwargs)


def _init_langchain_chat_model(provider: str, model: str) -> BaseChatModel:
    if provider == FIREWORKS:
        if not os.environ.get("FIREWORKS_API_KEY"):
            os.environ["FIREWORKS_API_KEY"] = getpass.getpass("Enter API key for Fireworks AI: ")
        return ChatFireworks(model=model)
    elif provider == HYPERBOLIC:
        if not os.environ.get("OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")
        return ChatOpenAI(model=model, base_url="https://api.hyperbolic.xyz/v1")
    else:
        raise ValueError(
            f"Method to create a langchain chat model for {provider} is not defined. Create and pass ChatModel to NearAiLangchainOrchestrator constructor."  # noqa: E501
        )
