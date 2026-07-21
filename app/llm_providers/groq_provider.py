from groq import AsyncGroq

from app.core.config import settings
from app.llm_providers.base import BaseLLMProvider

MODEL = "openai/gpt-oss-120b"


class GroqProvider(BaseLLMProvider):
    def __init__(self):
        self._client = AsyncGroq(api_key=settings.groq_api_key)

    async def chat(self, messages: list[dict]) -> str:
        response = await self._client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        return response.choices[0].message.content

    async def stream_chat(self, messages: list[dict]):
        stream = await self._client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta