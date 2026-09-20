from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentReference:

    document_id: str
    name: str
    extension: str

    source_id: str
    source_type: str

    category: str

    location: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    version: str | None = None
    content_hash: str | None = None