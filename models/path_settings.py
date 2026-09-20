from dataclasses import dataclass

@dataclass
class PathSettings:

    sources_config: str
    metadata_file: str
    vector_store_root: str