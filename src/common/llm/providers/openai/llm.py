from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.common.llm.base_classes import BaseLlmProvider
from src.common.llm.registry import register_provider
from src.config import config

from .constants import PROVIDER


@register_provider("llm", PROVIDER)
class OpenAiLlmProvider(BaseLlmProvider):
    def __init__(
        self, model: str | None = None, temperature: float | None = None
    ):
        self._client = ChatOpenAI(
            model=model or config.OPENAI_LLM_MODEL,
            temperature=(
                temperature
                if temperature is not None
                else config.OPENAI_LLM_TEMPERATURE
            ),
            api_key=SecretStr(config.OPENAI_API_KEY),
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
