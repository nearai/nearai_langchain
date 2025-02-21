from typing import Any, Dict

from langchain_openai import ChatOpenAI
from nearai.agents.environment import Environment  # type: ignore
from pydantic import Field, model_validator


class RemoteNearAIChatModel(ChatOpenAI):
    """Remote NEAR AI chat model implementation with NEAR AI inference."""

    env: Environment = Field(exclude=True)
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
        env: Environment = values.get("env")

        model_for_inference = env.get_model_for_inference()
        values["model"] = model_for_inference

        # Get OpenAI clients
        root_client = env.openai
        root_async_client = env.async_openai

        # Set the clients
        values["root_client"] = root_client
        values["root_async_client"] = root_async_client
        values["client"] = root_client.chat.completions
        values["async_client"] = root_async_client.chat.completions

        return values

    @model_validator(mode="after")
    def validate_environment(self) -> "RemoteNearAIChatModel":
        """Override parent's validate_environment to skip API key validation."""
        return self

    @property
    def chat_open_ai_model(self) -> ChatOpenAI:
        """Returns self as this class now inherits from ChatOpenAI."""
        return self

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {"model_name": self.model_name}
