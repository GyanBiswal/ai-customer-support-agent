import json

from fastapi import APIRouter
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from app.agent.graph import agent_graph

router = APIRouter()


class ChatRequest(BaseModel):
    thread_id: str
    message: str


@router.post("/chat/stream")
async def chat_stream(payload: ChatRequest):
    config = {"configurable": {"thread_id": payload.thread_id}}
    inputs = {"messages": [{"role": "user", "content": payload.message}]}

    async def event_generator():
        try:
            async for mode, chunk in agent_graph.astream(
                inputs, config, stream_mode=["updates", "custom"]
            ):
                if mode == "updates":
                    node_name = list(chunk.keys())[0]
                    yield {"event": "node_done", "data": node_name}

                elif mode == "custom":
                    if chunk.get("type") == "token":
                        yield {"event": "token", "data": chunk["content"]}

            yield {"event": "done", "data": json.dumps({})}

        except Exception as e:
            yield {"event": "error", "data": json.dumps({"message": str(e)})}

    return EventSourceResponse(event_generator())