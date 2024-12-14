"""Define the state structures for the agent."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class SearchState(BaseModel):
    """Search state."""

    user_query: str
    filters: Optional[dict] = None
    results: Optional[List[dict]] = None
    status: str = "awaiting_input"
