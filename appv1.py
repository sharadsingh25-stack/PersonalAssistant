from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompts.prompt import prompt
from knowledge_source.base_loader import BaseLoader
from splitter.split_chuncks import split_documents
from embeddings.faiss_store import create_faiss_index
from retriver.retriver import get_retriever
from chains.rag_chain import chain

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

chunks=split_documents()
faiss_index=create_faiss_index(chunks)
retriever=get_retriever(faiss_index)
while True:

    question = input("\nAsk a Question : ")

    if question.lower() == "exit":
        break

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    response = chain.invoke(
        {
            "context": context,
            "question": question
        }
    )

    print("\nAnswer\n")
    print(response)


# parser= StrOutputParser()
# chain=prompt | llm | parser

# response = chain.invoke({"question": "what is artificial intelligence?"})

# print(response)