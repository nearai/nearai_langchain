from functools import cached_property
from typing import Dict

from nearai_langchain.config import NEAR_AI_CONFIG
from nearai_langchain.constants import FIREWORKS, HYPERBOLIC


class NearAIAgentData:
    agent_metadata: Dict

    def __init__(self, agent_metadata: Dict) -> None:
        """Initialize agent data.

        Args:
        ----
            agent_metadata: Metadata for the agent.

        """
        self.agent_metadata = agent_metadata

    @cached_property
    def inference_framework(self) -> str:  # noqa: D102
        details = self.agent_metadata.get("details", {})
        agent = details.get("agent", {})
        defaults = agent.get("defaults", {})
        return defaults.get("inference_framework", "nearai")

    @cached_property
    def provider(self) -> str:  # noqa: D102
        details = self.agent_metadata.get("details", {})
        agent = details.get("agent", {})
        defaults = agent.get("defaults", {})
        provider = defaults.get("model_provider", "")
        if provider == "":
            model = self.metadata_model
            if FIREWORKS in model:
                provider = FIREWORKS
            if HYPERBOLIC in model:
                provider = HYPERBOLIC
        return provider

    @cached_property
    def metadata_model(self) -> str:  # noqa: D102
        details = self.agent_metadata.get("details", {})
        agent = details.get("agent", {})
        defaults = agent.get("defaults", {})
        return defaults.get("model", "")

    @cached_property
    def agent_id(self) -> str:  # noqa: D102
        account_id = NEAR_AI_CONFIG.get_account_id()
        name = self.agent_metadata.get("name", "")
        version = self.agent_metadata.get("version", "")
        return f"{account_id}/{name}/{version}"
