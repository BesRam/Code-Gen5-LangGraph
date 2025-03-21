import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from prompts.input_processing_prompt import input_processing_prompt


load_dotenv()

class InputProcessingAgent:
    def __init__(self, model_name: str = "gpt-4o", temperature: float = 0.0):
        """
        Initializes the agent with an OpenAI model.
        
        Args:
            model_name (str): The OpenAI model to use.
            temperature (float): The randomness level for responses.
        """
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")  # Fetch from .env
        )
        self.parser = JsonOutputParser()

    def process_input(self, user_input: str) -> dict:
        """
        Processes and classifies the user input using an LLM.

        Args:
            user_input (str): Raw input from the user.

        Returns:
            dict: Structured information with classification and extracted content.
        """
        prompt = input_processing_prompt.format(user_input=user_input)

        response = self.llm.invoke(prompt)
        result = self.parser.parse(response)

        return result
