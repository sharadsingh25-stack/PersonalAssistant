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


# --------------------------------------------------
# Configuration
# --------------------------------------------------

config_path = os.getenv(
    "APP_SETTINGS_PATH",
    DEFAULT_CONFIG
)

configuration_service = ConfigurationService(
    config_path
)

settings = configuration_service.load()


# --------------------------------------------------
# Embedding Model
# --------------------------------------------------

embedding_model = EmbeddingModel(
    settings.embedding.model
)

embeddings = embedding_model.get_embeddings()


# --------------------------------------------------
# Vector Store
# --------------------------------------------------

vector_store = VectorStore(
    embeddings,
    settings.paths.vector_store_root
)


# --------------------------------------------------
# Source Discovery
# --------------------------------------------------

source_service = SourceService(
    settings.paths.sources_config
)

sources = source_service.get_sources()


# --------------------------------------------------
# Document Splitter
# --------------------------------------------------

splitter = DocumentSplitter(
    settings.chunking.chunk_size,
    settings.chunking.chunk_overlap
)


# --------------------------------------------------
# Hash Store
# --------------------------------------------------

hash_store = HashStore(
    settings.paths.metadata_file
)


# ==================================================
# INGESTION
# ==================================================

for source in sources:

    print(
        f"\nProcessing: {source.name}"
    )

    # ----------------------------------------
    # Calculate current document hash
    # ----------------------------------------

    current_hash = DocumentHasher.calculate_hash(
        source.location
    )

    # ----------------------------------------
    # Check whether document changed
    # ----------------------------------------

    if not hash_store.is_changed(
        source.document_id,
        current_hash
    ):

        print(
            f"Skipping unchanged document: "
            f"{source.document_id}"
        )

        continue

    print(
        f"Processing changed/new document: "
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

        chunk.metadata["source_id"] = (
            source.source_id
        )

        chunk.metadata["source_type"] = (
            source.source_type
        )

        chunk.metadata["file_name"] = (
            source.name
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