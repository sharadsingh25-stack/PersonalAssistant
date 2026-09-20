from pathlib import Path

from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, embeddings, root_path: str):

        self.embeddings = embeddings
        self.root_path = Path(root_path)

    def upsert_documents(
        self,
        chunks,
        category: str,
        document_id: str
    ):

        store_path = self.root_path / category

        index_file = store_path / "index.faiss"

        # Create unique IDs for the chunks
        chunk_ids = [
            f"{document_id}_{index}"
            for index in range(len(chunks))
        ]

        # ------------------------------------------------
        # CASE 1: Category FAISS doesn't exist
        # ------------------------------------------------

        if not index_file.exists():

            print(
                f"Creating new vector store: {category}"
            )

            store_path.mkdir(
                parents=True,
                exist_ok=True
            )

            vector_store = FAISS.from_documents(
                chunks,
                self.embeddings,
                ids=chunk_ids
            )

        # ------------------------------------------------
        # CASE 2: Category FAISS already exists
        # ------------------------------------------------

        else:

            print(
                f"Loading existing vector store: {category}"
            )

            vector_store = FAISS.load_local(
                str(store_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )

            # --------------------------------------------
            # Find old chunks belonging to this document
            # --------------------------------------------

            old_ids = []

            for vector_id in vector_store.index_to_docstore_id.values():

                document = vector_store.docstore.search(
                    vector_id
                )

                if document is not None:

                    if (
                        document.metadata.get("document_id")
                        == document_id
                    ):
                        old_ids.append(vector_id)

            # --------------------------------------------
            # Remove old chunks
            # --------------------------------------------

            if old_ids:

                print(
                    f"Removing {len(old_ids)} old chunks "
                    f"from {document_id}"
                )

                vector_store.delete(
                    old_ids
                )

            # --------------------------------------------
            # Add new chunks
            # --------------------------------------------

            print(
                f"Adding {len(chunks)} new chunks "
                f"to {category}"
            )

            vector_store.add_documents(
                chunks,
                ids=chunk_ids
            )

        # ------------------------------------------------
        # Save updated FAISS index
        # ------------------------------------------------

        vector_store.save_local(
            str(store_path)
        )

        print(
            f"Vector store saved: {store_path}"
        )

        return vector_store

    def similarity_search(
        self,
        query: str,
        category: str,
        k: int = 5
        ):
        store_path = self.root_path / category

        index_file = store_path / "index.faiss"

        if not index_file.exists():
            raise FileNotFoundError(
                f"Vector store not found for category: {category}"
            )

        print(
            f"Loading vector store: {category}"
        )

        vector_store = FAISS.load_local(
            str(store_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )

        results = vector_store.similarity_search_with_score(
            query,
            k=k
        )

        return results