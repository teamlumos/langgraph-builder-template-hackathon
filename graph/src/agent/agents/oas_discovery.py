from gpt_researcher import GPTResearcher
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from graph.src.prompts.oas_discovery import oas_discovery_prompt, role_prompt

from .base import ResearchAgent


class OASDiscoveryAgent(ResearchAgent):
    """
    Agent that conducts OAS discovery.
    """

    def __init__(self, agent_model: str, service_name: str):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=oas_discovery_prompt(service_name=service_name),
            source_urls=None,
        )

    async def research(self) -> tuple[str, str]:
        researcher = GPTResearcher(
            query=self.prompt,
            report_type="custom_report",
        )

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        oas_url_list = self._get_oas_url(report)
        return report, oas_url_list

    def _get_oas_url(self, research_result: str) -> str:
        client = ChatOpenAI(
            model="gpt-4o-search-preview",
            web_search_options={"search_context_size": "high"},
        )

        prompt = PromptTemplate.from_template(
            role_prompt(service_name=self.service_name)
            + """
            
            List the most likely URLs with the official documentation for the latest OAS spec of this service, and explain why.

            Format as properly formatted MarkDown that includes the following keys: 
            - "url": Return only the URL
            - "confidence_level": Numeric confidence level: 1-4 (1 is lowest, 4 is highest)
            - "popularity": URL popularity as per Google rank: 1-4 (1 is lowest, 4 is highest)
            - "validated": Did you validate that OAS available through a web request? 1 = True, 0 = False
            - "explanation": Detailed explanation

            <research_result>
            {research_result}
            </research_result>
            """
        )

        chain = prompt | client | StrOutputParser()
        response = chain.invoke(research_result)
        return response
