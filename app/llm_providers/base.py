from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict]) -> str:
        """Non-streaming completion. Returns the assistant's text."""

    @abstractmethod
    async def stream_chat(self, messages: list[dict]):
        """Async generator yielding text chunks as they arrive."""