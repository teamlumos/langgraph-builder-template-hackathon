from typing import Dict, Any
from .state import State
from langchain_core.runnables import RunnableConfig
from abc import ABC, abstractmethod

from graph.src.prompts.pre_research import pre_research_prompt
from graph.src.prompts.product_req_research import product_req_research_prompt
from graph.src.prompts.sdk_open_api import initial_read_prompt
from graph.src.agent.utils import compose_prompt
from gpt_researcher import GPTResearcher
from graph.src.prompts.dev_req_research import dev_req_research_prompt
from graph.src.prompts.oas_retrieval import oas_retrieval_prompt

class ResearchAgent(ABC):
    """
    Base class for all research agents.
    """
    def __init__(self, agent_model: str, service_name: str,prompt: str, source_urls: list[str]):
        self.agent_model = agent_model
        self.service_name = service_name
        self.prompt = prompt
        self.source_urls = source_urls

    @abstractmethod
    async def research(self) -> tuple[str, str]:
        pass

class PreResearchAgent(ResearchAgent):
    """
    Agent that conducts pre-research, finding relevant endpoints and resources.
    """
    def __init__(self, agent_model: str, service_name: str, source_urls: list[str]):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=pre_research_prompt(),
            source_urls=source_urls
        )

    async def research(self) -> tuple[str, str]:
        researcher = GPTResearcher(
            query=self.prompt,
            report_type="custom_report",
            agent=self.agent_model,
            source_urls=self.source_urls,
        )

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report

class ProductReqResearchAgent(ResearchAgent):
    """
    Agent that conducts product requirements research.
    """
    def __init__(self, agent_model: str, service_name: str, source_urls: list[str], pre_research: str):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=product_req_research_prompt(service_name=service_name),
            source_urls=source_urls
        )
        self.pre_research = pre_research

    async def research(self) -> tuple[str, str]:
        sdk_prompt = initial_read_prompt(service_name=self.service_name)
        prompt = compose_prompt(
            pre_research=self.pre_research,
            sdk_prompt=sdk_prompt,
            product_req_prompt=self.prompt
        )
        researcher = GPTResearcher(
            query=prompt,
            report_type="custom_report",
            agent=self.agent_model,
            source_urls=self.source_urls,
        )

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report
    
class DevReqResearchAgent(ResearchAgent):
    """
    Agent that conducts developer requirements research.
    """
    def __init__(self, agent_model: str, service_name: str, source_urls: list[str], pre_research: str):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=dev_req_research_prompt(),
            source_urls=source_urls
        )
        self.pre_research = pre_research

    async def research(self) -> tuple[str, str]:
        sdk_prompt = initial_read_prompt(service_name=self.service_name)
        prompt = compose_prompt(
            pre_research=self.pre_research,
            sdk_prompt=sdk_prompt,
            dev_req_prompt=self.prompt
        )
        researcher = GPTResearcher(
            query=prompt,
            report_type="custom_report",
            agent=self.agent_model,
            source_urls=self.source_urls,
        )

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report

class OASRetrievalAgent(ResearchAgent):
    """
    Agent that retrieves the OpenAPI Specification (OAS) URL.
    """
    def __init__(self, agent_model: str, service_name: str, source_urls: list[str]):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=oas_retrieval_prompt(),
            source_urls=source_urls
        )

    async def research(self) -> tuple[str, str]:
        researcher = GPTResearcher(
            query=self.prompt,
            report_type="custom_report",
            agent=self.agent_model,
            source_urls=self.source_urls,
        )   

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report