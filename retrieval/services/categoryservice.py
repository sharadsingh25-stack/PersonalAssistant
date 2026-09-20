from services.sourceservice import SourceService


class CategoryService:

    def __init__(self, sources_config_path: str):
        self.source_service = SourceService(
            sources_config_path
        )

    def get_categories(self) -> list[str]:

        documents = self.source_service.get_sources()

        categories = {
            document.category
            for document in documents
            if document.category
        }

        return sorted(categories)