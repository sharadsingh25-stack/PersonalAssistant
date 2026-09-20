from dataclasses import dataclass

from models.path_settings import PathSettings
from models.embeddingsettings import EmbeddingSettings
from models.chunkingsettings import ChunkingSettings

@dataclass
class ApplicationSettings:

    paths: PathSettings

    embedding: EmbeddingSettings

    chunking: ChunkingSettings