from knowledge_source.pdf_loader import PdfLoader
from knowledge_source.word_loader import WordLoader
class LoaderFactory:

    _loaders = {
        ".pdf": PdfLoader,
        ".docx": WordLoader,
        ".doc": WordLoader
    }

    @classmethod
    def get_loader(cls, document):

        extension = document.extension.lower()

        loader_class = cls._loaders.get(
            extension
        )

        if loader_class is None:
            raise ValueError(
                f"Unsupported document type: "
                f"{extension}"
            )

        return loader_class(document)