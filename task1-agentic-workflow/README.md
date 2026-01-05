# Agentic Product Workflow – LangChain

## Overview
This project demonstrates a simple yet production-style agentic workflow using
LangChain AgentExecutor and OpenAI LLMs.

The agent autonomously decides whether to:
- Summarize a product title
- Classify a product
- Extract structured product attributes

## Key Features
- LLM-based decision making
- Deterministic tool execution
- Confidence-scored classification
- Regex + heuristic-based attribute extraction
- Bounded decision loop with clear stop condition

## Architecture
See `diagrams/architecture.txt`

## How to Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key_here
python main.py
