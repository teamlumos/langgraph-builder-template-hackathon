from abc import ABC, abstractmethod
from typing import Any, Dict

from gpt_researcher import GPTResearcher
from langchain_core.runnables import RunnableConfig

from graph.src.agent.utils import compose_prompt
from graph.src.prompts.dev_req_research import dev_req_research_prompt
from graph.src.prompts.oas_retrieval import oas_retrieval_prompt
from graph.src.prompts.pre_research import pre_research_prompt
from graph.src.prompts.product_req_research import product_req_research_prompt
from graph.src.prompts.sdk_open_api import initial_read_prompt

from .agents.dev_requirement_research import DevReqResearchAgent
from .agents.oas_discovery import OASDiscoveryAgent
from .agents.oas_retrieval import OASRetrievalAgent
from .agents.pre_research import PreResearchAgent
from .agents.product_requirements import ProductReqResearchAgent
from .state import State
