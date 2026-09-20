from knowledge_source.folder_source import FolderSource


class SourceFactory:

    @staticmethod
    def create(config):

        source_type = config.source_type.lower()

        if source_type == "folder":
            return FolderSource(config)

        raise ValueError(
            f"Unsupported source type: {config.source_type}"
        )