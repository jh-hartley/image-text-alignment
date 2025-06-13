from typing import TypeVar

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr

from src.common.new_llm.base_llm import BaseLlmProvider
from src.common.new_llm.registry import register_llm_provider
from src.config import config

T = TypeVar("T", bound=BaseModel)


@register_llm_provider("openai")
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

    def invoke(self, system: str, human: str) -> str:
        messages = [SystemMessage(content=system), HumanMessage(content=human)]
        response = self._client.invoke(messages)
        return response.content  # type: ignore

    async def ainvoke(self, system: str, human: str) -> str:
        messages = [SystemMessage(content=system), HumanMessage(content=human)]
        response = await self._client.ainvoke(messages)
        return response.content  # type: ignore
