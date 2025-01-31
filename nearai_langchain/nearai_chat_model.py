import json
import os
from functools import cached_property
from typing import Any, Dict, List, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.outputs import ChatResult
from langchain_openai import ChatOpenAI
from pydantic import Field

from nearai_langchain.agent_data import NearAIAgentData
from nearai_langchain.config import NEAR_AI_CONFIG


class NearAIChatModel(BaseChatModel):
    """NEAR AI chat model implementation with NEAR AI inference."""

    agent_data: NearAIAgentData = Field(...)
    runner_api_key: str = Field(default="", exclude=True)
    auth: str = Field(default="", exclude=True)

    def model_post_init(self, *args: Any, **kwargs: Any) -> None:
        """Initialize after Pydantic initialization."""
        super().model_post_init(*args, **kwargs)
        self._generate_auth_for_current_agent(NEAR_AI_CONFIG.client_config())

    def _generate_auth_for_current_agent(self, config):
        """Regenerate auth for the current agent."""
        if config.auth is not None:
            auth_bearer_token = config.auth.generate_bearer_token()
            new_token = json.loads(auth_bearer_token)
            new_token["runner_data"] = json.dumps(
                {"agent": self.agent_data.agent_id, "runner_api_key": self.runner_api_key}
            )
            auth_bearer_token = json.dumps(new_token)
            self.auth = auth_bearer_token
        else:
            self.auth = ""

    @cached_property
    def inference_model(self) -> str:
        """Returns 'provider::model_full_path'."""
        provider = self.agent_data.provider
        model = self.agent_data.metadata_model
        _, model_for_inference = NEAR_AI_CONFIG.provider_models.match_provider_model(model, provider)
        return model_for_inference

    @cached_property
    def chat_open_ai_model(self) -> ChatOpenAI:  # noqa: D102
        os.environ["OPENAI_API_KEY"] = self.auth
        return ChatOpenAI(model=self.inference_model, base_url=NEAR_AI_CONFIG.client_config().base_url)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate chat model outputs."""
        return self.chat_open_ai_model._generate(messages=messages, stop=stop, run_manager=run_manager, **kwargs)

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Asynchronously generate chat model outputs."""
        return await self.chat_open_ai_model._agenerate(messages=messages, stop=stop, run_manager=run_manager, **kwargs)

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get the identifying parameters."""
        return {"agent_data": self.agent_data}

    @property
    def _llm_type(self) -> str:
        """Get the type of LLM."""
        return "nearai-chat"
