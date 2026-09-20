from langchain_community.document_loaders import Docx2txtLoader

from knowledge_source.base_loader import BaseLoader
from models.document_reference import DocumentReference

class WordLoader(BaseLoader):
    def __init__(self, document: DocumentReference):
    
            if not document.location:
                raise ValueError(
                    "PDF document requires a location."
                )
    
            self.document = document

    def load(self):

        loader = Docx2txtLoader(
            self.document.location
        )

        return loader.load()