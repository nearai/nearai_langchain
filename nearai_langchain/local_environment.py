import logging
from typing import Any, Iterable, List, Literal, Optional, Union

from openai import NOT_GIVEN, NotGiven
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.message_create_params import Attachment

from nearai_langchain.config import NEAR_AI_CONFIG


class LocalEnvironment(object):
    """Local lightweight environment class for local runs."""

    def __init__(self, thread_id: str, agent_id: str):  # noqa: D107
        self.hub_client = NEAR_AI_CONFIG.get_hub_client()
        self.agent_id = agent_id
        if thread_id:
            thread = self.hub_client.beta.threads.retrieve(thread_id)
        else:
            thread = self.hub_client.beta.threads.create()
            print(f"New thread created with thread_id={thread.id}")
        self.thread_id = thread.id

        self.run = self.hub_client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.agent_id,
            extra_body={"delegate_execution": True},
        )

    def add_user_message(self, message: str) -> None:
        """Adds a user message to thread."""
        self.hub_client.beta.threads.messages.create(thread_id=self.thread_id, role="user", content=message)

    def _list_messages(
        self,
        limit: Union[int, NotGiven] = NOT_GIVEN,
        order: Literal["asc", "desc"] = "asc",
        thread_id: Optional[str] = None,
    ) -> List[Message]:
        """Returns messages from the environment."""
        messages = self.hub_client.beta.threads.messages.list(
            thread_id=thread_id or self.thread_id, limit=limit, order=order
        )
        return messages.data

    def add_reply(
        self,
        message: str,
        attachments: Optional[Iterable[Attachment]] = None,
        message_type: Optional[str] = None,
    ):
        """Assistant adds a message to the environment."""
        return self.hub_client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="assistant",
            content=message,
            extra_body={
                "assistant_id": self.agent_id,
                "run_id": self.run.id,
            },
            attachments=attachments,
            metadata={"message_type": message_type} if message_type else None,
        )

    def list_messages(self, thread_id: Optional[str] = None):
        """Backwards compatibility for chat_completions messages."""
        messages = self._list_messages(thread_id=thread_id)

        # Filter out system and agent log messages when running in debug mode. Agent behavior shouldn't change based on logs.  # noqa: E501
        legacy_messages = [
            {
                "id": m.id,
                "content": "\n".join([c.text.value for c in m.content]),  # type: ignore
                "role": m.role,
            }
            for m in messages
        ]
        return legacy_messages

    def get_last_message(self, role: str = "user"):
        """Reads last message from the given role and returns it."""
        for message in reversed(self.list_messages()):
            if message.get("role") == role:
                return message

        return None

    def add_message(
        self,
        role: str,
        message: str,
        attachments: Optional[Iterable[Attachment]] = None,
        **kwargs: Any,
    ):
        """Deprecated. Please use `add_reply` instead. Assistant adds a message to the environment."""
        return self.add_reply(message, attachments, **kwargs)

    def request_user_input(self) -> None:  # noqa: D102
        pass

    def mark_done(self) -> None:  # noqa: D102
        pass

    def mark_failed(self) -> None:  # noqa: D102
        pass

    def add_system_log(self, log: str, level: int = logging.INFO) -> None:  # noqa: D102
        pass

    def add_agent_log(self, log: str, level: int = logging.INFO) -> None:  # noqa: D102
        pass
