from dataclasses import dataclass

@dataclass
class EmbeddingSettings:

    provider: str

    model: str