from langgraph.types import StreamWriter

from app.agent.state import AgentState
from app.llm_providers.groq_provider import GroqProvider

llm = GroqProvider()

SYSTEM_PROMPT = (
    "You are a helpful AI customer support agent. "
    "Answer the user's message clearly and concisely."
)


async def plan_node(state: AgentState, writer: StreamWriter) -> dict:
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in state["messages"]:
        role = "user" if msg.type == "human" else "assistant"
        history.append({"role": role, "content": msg.content})

    full_reply = ""

    async for chunk in llm.stream_chat(history):
        full_reply += chunk
        writer({"type": "token", "content": chunk})

    return {
        "messages": [{"role": "assistant", "content": full_reply}],
        "next_action": "respond",
    }