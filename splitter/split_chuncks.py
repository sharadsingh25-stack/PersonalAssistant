from langchain_text_splitters  import RecursiveCharacterTextSplitter
from knowledge_source.loader_factory import LoaderFactory

def split_documents():
    documents = LoaderFactory.get_loader("pdf", "data/Employee_Handbook_RAG_Practice.pdf").load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    return chunks