from abc import ABC, abstractmethod
from models.sourceconfig import SourceConfig


class BaseSource(ABC):

    def __init__(self, config: SourceConfig):
        self.config = config

    @abstractmethod
    def discover_documents(self):
        """
        Discover documents available from the source.
        """
        pass