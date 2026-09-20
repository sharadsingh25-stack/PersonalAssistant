from pydantic import BaseModel, Field

from agents.rag.state import AgentState
from retrieval.services.categoryservice import CategoryService


class RouteDecision(BaseModel):

    category: str = Field(
        description="The knowledge category that should be searched."
    )


class QueryRouter:

    def __init__(
        self,
        llm,
        category_service: CategoryService
    ):
        self.llm = llm
        self.category_service = category_service

    def route(
        self,
        question: str
    ) -> str:

        categories = (
            self.category_service.get_categories()
        )

        if not categories:
            raise ValueError(
                "No knowledge categories are available."
            )

        categories_text = ", ".join(categories)

        structured_llm = self.llm.with_structured_output(
            RouteDecision
        )

        prompt = f"""
You are a routing component for an enterprise
knowledge-base RAG system.

Your job is ONLY to determine which knowledge
category should be searched.

Available categories:
{categories_text}

User question:
{question}

Rules:
1. Select exactly one category from the available categories.
2. Do not answer the user's question.
3. Do not use general knowledge to answer the question.
4. Choose the category whose knowledge source is most
   relevant to the question.
"""

        result = structured_llm.invoke(prompt)

        category = result.category.strip()

        if category not in categories:
            raise ValueError(
                f"Router returned invalid category: {category}"
            )

        return category


def query_router_node(
    state: AgentState,
    router: QueryRouter
) -> AgentState:

    category = router.route(
        state["question"]
    )

    return {
        "category": category
    }