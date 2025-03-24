from gpt_researcher import GPTResearcher

from graph.src.prompts.pre_research import pre_research_prompt

from .base import ResearchAgent


class PreResearchAgent(ResearchAgent):
    """
    Agent that conducts pre-research, finding relevant endpoints and resources.
    """

    def __init__(self, agent_model: str, service_name: str, html: str):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=pre_research_prompt(html),
            source_urls=None,
        )

    async def research(self) -> tuple[str, str]:
        researcher = GPTResearcher(
            query=self.prompt,
            report_type="custom_report",
            agent=self.agent_model,
            source_urls=self.source_urls,
            verbose=True,
        )

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report
