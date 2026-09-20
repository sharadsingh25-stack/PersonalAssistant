from vectorstores.vectorstores import VectorStore


class RetrieverService:

    def __init__(
        self,
        vector_store: VectorStore,
        top_k: int = 5
    ):
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(
        self,
        question: str,
        category: str
    ):

        if not question:
            raise ValueError(
                "Question is required for retrieval."
            )

        if not category:
            raise ValueError(
                "Category is required for retrieval."
            )

        documents = self.vector_store.similarity_search(
            query=question,
            category=category,
            k=self.top_k
        )

        return documents