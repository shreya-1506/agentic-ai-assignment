from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

from agent.tools import (
    summarize_product,
    classify_product,
    extract_product_attributes
)


def create_agent():
    """
    Creates and returns a LangChain AgentExecutor with
    robust exception handling and a bounded decision loop.
    """

    try:
        # -----------------------------
        # Tool Definitions
        # -----------------------------
        tools = [
            Tool(
                name="SummarizeProduct",
                func=summarize_product,
                description=(
                    "Summarize a long or complex product title. "
                    "Use only when the title is verbose."
                )
            ),
            Tool(
                name="ClassifyProduct",
                func=classify_product,
                description=(
                    "Classify a product into category and sub-category "
                    "with a confidence score. Use when no clear specs exist."
                )
            ),
            Tool(
                name="ExtractProductAttributes",
                func=extract_product_attributes,
                description=(
                    "Extract structured attributes such as brand, model, "
                    "memory, color using deterministic logic."
                )
            )
        ]

        # -----------------------------
        # LLM Configuration
        # -----------------------------
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0
        )

        # -----------------------------
        # Agent Prompt (Decision Logic)
        # -----------------------------
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """
                You are an intelligent product-processing agent.

                Your responsibilities:
                1. Read the product title carefully
                2. Decide which ONE tool to use:
                - SummarizeProduct
                - ClassifyProduct
                - ExtractProductAttributes
                3. Invoke the chosen tool
                4. Return the tool output and STOP

                Decision Rules:
                - Prefer ExtractProductAttributes if specifications or attributes are present
                - Prefer SummarizeProduct if the title is long or complex
                - Otherwise, use ClassifyProduct

                IMPORTANT:
                - Call only ONE tool
                - Do not invent data
                - Stop after producing the final result
                """
            ),
            ("human", "{input}")
        ])

        # -----------------------------
        # Create Agent
        # -----------------------------
        agent = create_tool_calling_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
        )

        # -----------------------------
        # Agent Executor (Stop Condition)
        # -----------------------------
        return AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=2,  # clear stop condition
            handle_parsing_errors=True
        )

    except Exception as e:
        raise RuntimeError(
            f"Agent initialization failed: {str(e)}"
        )
