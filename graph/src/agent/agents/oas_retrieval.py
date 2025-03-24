from gpt_researcher import GPTResearcher

from graph.src.prompts.oas_retrieval import oas_retrieval_prompt

from .base import ResearchAgent


class OASRetrievalAgent(ResearchAgent):
    """
    Agent that retrieves the OpenAPI Specification (OAS) URL.
    """

    def __init__(self, agent_model: str, service_name: str, source_urls: list[str]):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=oas_retrieval_prompt(),
            source_urls=source_urls,
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
