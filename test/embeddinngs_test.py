from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

query = "What is the purpose of this document?"

query_embedding = embeddings.embed_query(query)

print("Query embedding:", query_embedding)