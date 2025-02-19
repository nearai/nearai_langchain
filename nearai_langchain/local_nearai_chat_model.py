import json
from typing import Any, Dict

from langchain_openai import ChatOpenAI
from pydantic import Field, model_validator

from nearai_langchain.agent_data import NearAIAgentData
from nearai_langchain.local_config import LOCAL_NEAR_AI_CONFIG
from nearai_langchain.secure_openai_clients import SecureAsyncOpenAI, SecureOpenAI


class LocalNearAIChatModel(ChatOpenAI):
    """Local NEAR AI chat model implementation with NEAR AI inference."""

    agent_data: NearAIAgentData = Field(...)
    runner_api_key: str = Field(default="", exclude=True)
    auth: str = Field(default="", exclude=True)
    model_name: str = Field(default="gpt-3.5-turbo", alias="model")

    # Override the clients to use our custom setup
    client: Any = Field(default=None, exclude=True)
    async_client: Any = Field(default=None, exclude=True)
    root_client: Any = Field(default=None, exclude=True)
    root_async_client: Any = Field(default=None, exclude=True)

    @model_validator(mode="before")
    @classmethod
    def setup_auth(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Set up authentication before model initialization."""
        config = LOCAL_NEAR_AI_CONFIG.client_config()
        agent_data = values.get("agent_data")
        assert agent_data
        runner_api_key = values.get("runner_api_key", "")

        # Generate auth token
        if config.auth is not None and agent_data:
            auth_bearer_token = config.auth.generate_bearer_token()
            new_token = json.loads(auth_bearer_token)
            new_token["runner_data"] = json.dumps(
                {"agent": agent_data.agent_identifier, "runner_api_key": runner_api_key}
            )
            auth_bearer_token = json.dumps(new_token)
        else:
            auth_bearer_token = ""

        # Set up model values
        provider = agent_data.provider
        model = agent_data.metadata_model
        _, model_for_inference = LOCAL_NEAR_AI_CONFIG.provider_models.match_provider_model(model, provider)

        # Update values for ChatOpenAI initialization
        values["model"] = model_for_inference
        values["base_url"] = config.base_url
        values["auth"] = auth_bearer_token

        # Initialize the clients directly
        client_params = {
            "api_key": auth_bearer_token,  # Use our auth token as the API key
            "base_url": config.base_url,
            "default_headers": {"Authorization": f"Bearer {auth_bearer_token}"},
        }

        # Create OpenAI clients
        root_client = SecureOpenAI(**client_params)
        root_async_client = SecureAsyncOpenAI(**client_params)

        # Set the clients
        values["root_client"] = root_client
        values["root_async_client"] = root_async_client
        values["client"] = root_client.chat.completions
        values["async_client"] = root_async_client.chat.completions

        return values

    @model_validator(mode="after")
    def validate_environment(self) -> "LocalNearAIChatModel":
        """Override parent's validate_environment to skip API key validation."""
        return self

    @property
    def chat_open_ai_model(self) -> ChatOpenAI:
        """Returns self as this class now inherits from ChatOpenAI."""
        return self

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {"model_name": self.model_name, "agent_data": self.agent_data}
