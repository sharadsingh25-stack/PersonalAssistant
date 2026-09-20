from langchain_community.vectorstores import FAISS
from embeddings.embedding_model import EmbeddingModel


def create_faiss_index(chunks, model_name):

    embedding_model = EmbeddingModel(model_name)

    embeddings = embedding_model.get_embeddings()

    return FAISS.from_documents(
        chunks,
        embeddings
    )

# Old OpenAI embedding code, replaced with HuggingFace embeddings
# from langchain_community.vectorstores import FAISS
# from embeddings.embedding_model import get_embeddings

# def create_faiss_index(chunks):
#     embeddings = get_embeddings()
#     faiss_index = FAISS.from_documents(chunks, embeddings)
#     return faiss_index