from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModel:

    def __init__(self, model_name: str):
        self._embeddings = HuggingFaceEmbeddings(
            model_name=model_name
        )

    def get_embeddings(self):
        return self._embeddings



#OpenAI Embeddings Code
# from langchain_openai import OpenAIEmbeddings

# from dotenv import load_dotenv

# load_dotenv()
# def get_embeddings():
#     embeddings = OpenAIEmbeddings(
#         model="text-embedding-3-small"
#     )
#     return embeddings
    

