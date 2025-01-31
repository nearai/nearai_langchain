import shlex
import sys
from functools import cached_property

import fire  # type: ignore
import openai
from nearai.cli import LoginCLI  # type: ignore

# from nearai.config import load_config
from nearai.config import CONFIG  # type: ignore
from nearai.shared.client_config import ClientConfig  # type: ignore
from nearai.shared.provider_models import ProviderModels  # type: ignore
from openai import OpenAI


class CLI:
    def __init__(self) -> None:  # noqa: D107
        self.login = LoginCLI()


class NearAIConfig:
    def __init__(self) -> None:  # noqa: D107
        # self.config = load_config()
        self.config = CONFIG
        pass

    def client_config(self) -> ClientConfig:  # noqa: D102
        if self.config.auth is None:
            print("NearAI authentication required. Running web-based login...")
            command = "nearai login --remote"
            sys.argv = shlex.split(command)
            fire.Fire(CLI)

            # Note: At this point, the user needs to:
            # 1. Follow the auth URL that will be printed
            # 2. Complete the authentication process
            # 3. Get the login save command with parameters

            save_command = input("Please enter the login save command: ")
            sys.argv = shlex.split(save_command)  # Properly splits command respecting quotes
            fire.Fire(CLI)

            # self.config = load_config()

        return self.config.get_client_config()

    def get_hub_client(self) -> OpenAI:  # noqa: D102
        config = self.client_config()
        signature = config.auth.model_dump_json()
        base_url = config.base_url
        return openai.OpenAI(base_url=base_url, api_key=signature)

    def get_account_id(self) -> str:  # noqa: D102
        config = self.client_config()
        return config.auth.account_id

    @cached_property
    def provider_models(self) -> ProviderModels:  # noqa: D102
        return ProviderModels(self.client_config())


NEAR_AI_CONFIG = NearAIConfig()
