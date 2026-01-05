import json
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

def generate_description(title: str, supplier_text: str | None, strategy: str) -> str:
    """
    Generates a product description using controlled LLM prompting.
    Always returns JSON (as string).
    """

    try:
        if not title or not isinstance(title, str):
            raise ValueError("Invalid product title")

        prompt = ChatPromptTemplate.from_messages([
            ("system",
             """
        You are a responsible product description generator.

        CRITICAL RULES:
        - DO NOT invent product attributes
        - Use ONLY information present in input
        - If assumptions are unavoidable, list them explicitly
        - Output MUST be valid JSON
        """),
                    ("human",
                    f"""
        Product Title:
        {title}

        Supplier Information:
        {supplier_text}

        Generation Strategy:
        {strategy}

        Return JSON with EXACT keys:
        - product_title
        - description
        - assumptions (array)
        - validation (object, initially empty)
        """)
        ])

        response = llm.invoke(prompt.format_messages())
        return response.content

    except Exception as e:
        return json.dumps({
            "product_title": title,
            "description": "",
            "assumptions": [],
            "validation": {
                "error": f"Generation failed: {str(e)}"
            }
        })
