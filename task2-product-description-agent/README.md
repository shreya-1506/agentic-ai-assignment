# AI-Based Product Description Generator

## Overview
This project implements a decision-driven AI system that generates product
descriptions responsibly using LLMs.

The system does NOT blindly generate text. Instead, it:
- Analyzes input completeness
- Selects a generation strategy
- Enforces hallucination control
- Produces structured JSON output

## Key Constraints Addressed
- No invented attributes
- Explicit assumptions
- Visible decision logic
- Valid JSON output
- Validation and refinement step

## How to Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
python main.py
