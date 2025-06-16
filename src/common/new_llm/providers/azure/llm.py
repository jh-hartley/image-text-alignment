from typing import TypeVar, cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel, SecretStr

from src.common.new_llm.base_classes import BaseLlmProvider
from src.common.new_llm.registry import register_provider
from src.config import config

from .constants import PROVIDER

T = TypeVar("T", bound=BaseModel)


class MessageContent(BaseModel):
    type: str
    text: str | None = None
    image_url: dict[str, str] | None = None


@register_provider("llm", PROVIDER)
class AzureLlmProvider(BaseLlmProvider):
    def __init__(
        self, model: str | None = None, temperature: float | None = None
    ):
        self._client = AzureChatOpenAI(
            model=model or config.AZURE_OPENAI_DEPLOYMENT,
            temperature=(
                temperature
                if temperature is not None
                else config.OPENAI_LLM_TEMPERATURE
            ),
            api_key=SecretStr(config.AZURE_OPENAI_API_KEY),
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            api_version=config.AZURE_OPENAI_API_VERSION,
            azure_deployment=config.AZURE_OPENAI_DEPLOYMENT,
        )

    def invoke(
        self, system: str, human: str, images: list[str] | None = None
    ) -> str:
        system_msg = SystemMessage(content=system)

        if images:
            human_msg = HumanMessage(
                content=[
                    {"type": "text", "text": human},
                    *[
                        {"type": "image_url", "image_url": {"url": url}}
                        for url in images
                    ],
                ]
            )
        else:
            human_msg = HumanMessage(content=human)

        messages = [system_msg, human_msg]
        response = self._client.invoke(messages)
        return cast(str, response.content)

    async def ainvoke(
        self, system: str, human: str, images: list[str] | None = None
    ) -> str:
        system_msg = SystemMessage(content=system)

        if images:
            human_msg = HumanMessage(
                content=[
                    {"type": "text", "text": human},
                    *[
                        {"type": "image_url", "image_url": {"url": url}}
                        for url in images
                    ],
                ]
            )
        else:
            human_msg = HumanMessage(content=human)

        messages = [system_msg, human_msg]
        response = await self._client.ainvoke(messages)
        return cast(str, response.content)
