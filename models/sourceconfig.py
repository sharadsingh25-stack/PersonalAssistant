from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceConfig:
    source_id: str
    source_type: str
    enabled: bool
    settings: dict[str, Any] = field(default_factory=dict)


@dataclass
class SourceConfigRoot:
    sources: list[SourceConfig]