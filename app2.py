import os
from embeddings.embedding_model import EmbeddingModel
from services.configurationservice import ConfigurationService
from services.sourceservice import SourceService
from services.documentsplitter import DocumentSplitter
from knowledge_source.loader_factory import LoaderFactory
from services.documenthasher import DocumentHasher
from services.hashstore import HashStore
from vectorstores.vectorstores import VectorStore
 
DEFAULT_CONFIG = "config/appsetting.json"

config_path = os.getenv(
    "APP_SETTINGS_PATH",
    DEFAULT_CONFIG
)


configuration_service = ConfigurationService(config_path)

settings = configuration_service.load()
embedding_model = EmbeddingModel(
    settings.embedding.model
)

embeddings = embedding_model.get_embeddings()
vector_store = VectorStore(
    embeddings,
    settings.paths.vector_store_root
)

source_service = SourceService(
    settings.paths.sources_config
)

sources = source_service.get_sources()

splitter = DocumentSplitter(
    settings.chunking.chunk_size,
    settings.chunking.chunk_overlap
)

hash_store = HashStore(
    settings.paths.metadata_file
)

for source in sources:

    current_hash = DocumentHasher.calculate_hash(
    source.config["path"]
    )

    # ----------------------------------------
    # Check whether document changed
    # ----------------------------------------

    if not hash_store.is_changed(
        source.document_id,
        current_hash
    ):

        print(
            f"Skipping unchanged source: "
            f"{source.document_id}"
        )

        continue

    print(
        f"Processing source: "
        f"{source.document_id}"
    )

    # ----------------------------------------
    # Load
    # ----------------------------------------

    loader = LoaderFactory.get_loader(
    source
    )

    documents = loader.load()

    # ----------------------------------------
    # Split
    # ----------------------------------------

    chunks = splitter.split(
        documents
    )

    # ----------------------------------------
    # Add metadata
    # ----------------------------------------

    for chunk in chunks:

        chunk.metadata["document_id"] = (
            source.document_id
        )

        chunk.metadata["category"] = (
            source.category
        )

    print(
        f"Documents: {len(documents)}"
    )

    print(
        f"Chunks: {len(chunks)}"
    )

    # ----------------------------------------
    # Create / Update Vector Store
    # ----------------------------------------

    vector_store.upsert_documents(
        chunks,
        source.category,
        source.document_id
    )

    # ----------------------------------------
    # Save hash ONLY after success
    # ----------------------------------------

    hash_store.save_hash(
        source.document_id,
        current_hash
    )

    print(
        f"Completed: {source.document_id}"
    )