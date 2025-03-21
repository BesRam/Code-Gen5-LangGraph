"""
LLM Feedback Scoring Strategy:
Uses an LLM to rate the code's clarity, readability, and quality on a 0 to 10 scale.
"""

import os
import re
from dotenv import load_dotenv
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

# Prompt template
feedback_prompt = PromptTemplate.from_template("""
You are a code reviewer.

Evaluate the following Python function and assign a score from 0 to 10 based on:
- Clarity and readability
- Proper use of comments and structure
- Code style and cleanliness
- Overall implementation quality

### Code:
```python
{code}
                                               
Respond only with a single integer number (0 to 10). """)

class LLMFeedbackScoringStrategy: 
    def __init__(self, model_name="gpt-4o", temperature=0.0): 
        self.llm = ChatOpenAI( 
            model=model_name, 
            temperature=temperature, 
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def name(self) -> str:
        return "llm_feedback"
    
    def score(self, codes: List[str]) -> List[float]:
        scores = []
        for code in codes:
            prompt = feedback_prompt.format(code=code)
            response = self.llm.invoke(prompt).content

            try:
                match = re.search(r"\d+", response)
                if match:
                    numeric = int(match.group())
                    normalized = min(max(numeric / 10, 0.0), 1.0)
                else:
                    normalized = 0.0
            except:
                normalized = 0.0

            scores.append(normalized)
        return scores