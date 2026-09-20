import json

from models.sourceconfig import SourceConfig
from knowledge_source.source_factory import SourceFactory


class SourceService:

    def __init__(self, config_path: str):
        self.config_path = config_path

    def get_sources(self):

        with open(
            self.config_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        documents = []

        for item in data.get("sources", []):

            # ----------------------------------------
            # Check whether source is enabled
            # ----------------------------------------

            if not item.get("enabled", True):
                continue

            # ----------------------------------------
            # Create SourceConfig
            # ----------------------------------------

            config = SourceConfig(
                source_id=item["sourceId"],
                source_type=item["sourceType"],
                enabled=item.get("enabled", True),
                settings=item.get("settings", {})
            )

            # ----------------------------------------
            # Create source implementation
            # ----------------------------------------

            source = SourceFactory.create(config)

            # ----------------------------------------
            # Discover documents
            # ----------------------------------------

            discovered_documents = (
                source.discover_documents()
            )

            documents.extend(
                discovered_documents
            )

        return documents