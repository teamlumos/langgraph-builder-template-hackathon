from gpt_researcher import GPTResearcher

from graph.src.agent.utils import compose_prompt
from graph.src.prompts.dev_req_research import dev_req_research_prompt
from graph.src.prompts.sdk_open_api import initial_read_prompt

from .base import ResearchAgent


class DevReqResearchAgent(ResearchAgent):
    """
    Agent that conducts developer requirements research.
    """

    def __init__(
        self,
        agent_model: str,
        service_name: str,
        source_urls: list[str],
        pre_research: str,
    ):
        super().__init__(
            agent_model=agent_model,
            service_name=service_name,
            prompt=dev_req_research_prompt(),
            source_urls=source_urls,
        )
        self.pre_research = pre_research

    async def research(self) -> tuple[str, str]:
        sdk_prompt = initial_read_prompt(service_name=self.service_name)
        prompt = compose_prompt(
            pre_research=self.pre_research,
            sdk_prompt=sdk_prompt,
            dev_req_prompt=self.prompt,
        )
        researcher = GPTResearcher(
            query=prompt,
            report_type="custom_report",
            agent=self.agent_model,
            source_urls=self.source_urls,
            verbose=False,
        )

        research_result = await researcher.conduct_research()
        report = await researcher.write_report()

        return research_result, report
