from typing import Annotated, Optional, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # Full conversation, reduced with LangGraph's built-in message merger
    messages: Annotated[list, add_messages]

    # Tool calls the plan node wants executed (empty in this phase)
    pending_tool_calls: list[dict]

    # Results of tool execution, fed back into the next plan step
    tool_results: list[dict]

    # Routing signal: "respond" | "call_tools" (only "respond" exists so far)
    next_action: Optional[str]