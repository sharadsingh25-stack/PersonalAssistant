import json

from models.sourceconfig import SourceConfig, SourceConfigRoot


class SourceConfigLoader:

    @staticmethod
    def load(file_path: str) -> SourceConfigRoot:

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        sources = [
            SourceConfig(
                source_id=item["sourceId"],
                source_type=item["sourceType"],
                enabled=item.get("enabled", True),
                settings=item.get("settings", {})
            )
            for item in data.get("sources", [])
        ]

        return SourceConfigRoot(sources=sources)