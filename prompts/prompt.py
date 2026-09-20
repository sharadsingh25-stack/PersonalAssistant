from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an HR assistant.

Answer the question ONLY using the context provided.

If the answer is not present in the context, say:
"I don't know based on the provided document."

Context:
{context}

Question:
{question}
""")