import json

from models.applicationsettings import ApplicationSettings
from models.chunkingsettings import ChunkingSettings
from models.embeddingsettings import EmbeddingSettings
from models.path_settings import PathSettings


class ConfigurationService:

    def __init__(self, config_path: str):
        self._config_path = config_path

    def load(self) -> ApplicationSettings:

        with open(self._config_path, "r") as file:
            data = json.load(file)

        return ApplicationSettings(
            paths=PathSettings(**data["paths"]),
            embedding=EmbeddingSettings(**data["embedding"]),
            chunking=ChunkingSettings(**data["chunking"])
        )