from abc import ABC, abstractmethod


class ResearchAgent(ABC):
    """
    Base class for all research agents.
    """

    def __init__(
        self, agent_model: str, service_name: str, prompt: str, source_urls: list[str]
    ):
        self.agent_model = agent_model
        self.service_name = service_name
        self.prompt = prompt
        self.source_urls = source_urls

    @abstractmethod
    async def research(self) -> tuple[str, str]:
        pass
