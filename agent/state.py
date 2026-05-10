"""AgentState TypedDict shared across graph nodes."""

import operator
from typing import Annotated, List

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    dataset_paths: List[str]
