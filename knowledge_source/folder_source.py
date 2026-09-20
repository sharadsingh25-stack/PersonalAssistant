from pathlib import Path

from knowledge_source.base_source import BaseSource
from models.document_reference import DocumentReference


class FolderSource(BaseSource):

    def discover_documents(self):

        path = self.config.settings["path"]

        recursive = self.config.settings.get(
            "recursive",
            True
        )

        root_path = Path(path)

        if not root_path.exists():
            raise FileNotFoundError(
                f"Source path does not exist: {root_path}"
            )

        if recursive:
            files = [
                file
                for file in root_path.rglob("*")
                if file.is_file()
            ]
        else:
            files = [
                file
                for file in root_path.glob("*")
                if file.is_file()
            ]

        documents = []

        for file in files:

            category = self._get_category(
                file,
                root_path
            )

            relative_path = file.relative_to(root_path)

            document = DocumentReference(
                document_id=str(relative_path).replace("\\", "/"),
                name=file.name,
                extension=file.suffix.lower(),
                source_id=self.config.source_id,
                source_type=self.config.source_type,
                category=category,
                location=str(file.resolve())
            )

            documents.append(document)

        return documents

    def _get_category(
        self,
        file: Path,
        root_path: Path
    ) -> str:

        strategy = self.config.settings.get(
            "categoryStrategy",
            "Folder"
        )

        if strategy.lower() == "folder":

            relative_path = file.relative_to(
                root_path
            )

            if len(relative_path.parts) > 1:
                return relative_path.parts[0]

            return "General"

        return "General"