from dataclasses import dataclass

@dataclass
class ChunkingSettings:

    chunk_size: int

    chunk_overlap: int