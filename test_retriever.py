from embeddings.embedding_model import EmbeddingModel
from services.configurationservice import ConfigurationService
from vectorstores.vectorstores import VectorStore
from retrieval.services.retrieverservice import RetrieverService


# ----------------------------------------
# Load configuration
# ----------------------------------------

configuration_service = ConfigurationService(
    "config/appsetting.json"
)

settings = configuration_service.load()


# ----------------------------------------
# Create embedding model
# ----------------------------------------

embedding_model = EmbeddingModel(
    settings.embedding.model
)

embeddings = embedding_model.get_embeddings()


# ----------------------------------------
# Create VectorStore
# ----------------------------------------

vector_store = VectorStore(
    embeddings,
    settings.paths.vector_store_root
)


# ----------------------------------------
# Create RetrieverService
# ----------------------------------------

retriever = RetrieverService(
    vector_store=vector_store,
    top_k=5
)


# ----------------------------------------
# Test query
# ----------------------------------------

question = "What is maternity leave policy??"

category = "HR"


documents = retriever.retrieve(
    question=question,
    category=category
)


# ----------------------------------------
# Display results
# ----------------------------------------

print()
print("========================================")
print("Retrieved Documents")
print("========================================")

for index, result in enumerate(documents, start=1):

    document, score = result

    print()
    print(f"Result {index}")
    print("----------------------------------------")

    print("Score:")
    print(score)

    print()
    print("Content:")
    print(document.page_content)

    print()
    print("Metadata:")
    print(document.metadata)