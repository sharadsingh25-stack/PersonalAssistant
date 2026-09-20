from abc import ABC, abstractmethod

from models.document_reference import DocumentReference


class BaseLoader(ABC):

    def __init__(self, document: DocumentReference):
        self.document = document

    @abstractmethod
    def load(self):
        pass