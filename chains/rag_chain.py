from langchain_core.output_parsers import StrOutputParser

from llms.llm_factory import get_llm
from prompts.prompt import prompt

llm = get_llm()

parser = StrOutputParser()

chain = prompt | llm | parser