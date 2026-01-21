# This is the function that starts a local AI model (LLM), connecting to external tools, and return the model with tools integrated

import os
from dotenv import load_dotenv # Import the function to load .env variables

from langchain_ollama import ChatOllama     # Import the Ollama Chat model

from tools.calculator import add, sub, mul, divide  # Import the calculator tools
from tools.cat_tools import get_random_cat_fact  # Import the cat fact tool

load_dotenv()  # Load environment variables from .env file

def get_llm_with_tools():

    """
        Starts local LLM (llama 3,1 via Ollama) 
        Returns: The model with tools integrated and the list of tools
    """

    # This is not really necessary, but helps to have the model name and temperature configurable via .env
    # but shows attention to security/best practices
    model_name = os.getenv("MODEL_NAME", "llama3.1")        # If not found, defaults to "llama3.1"
    temperature = float( os.getenv("TEMPERATURE", "0") )    # Default temperature is 0

    # Starts the local LLM via Ollama
    llm = ChatOllama(

        model = model_name,         # Local model
        temperature = temperature,  # temperature to 0 to make the model deterministic (logical)

    )

    tools = [ add, sub, mul, divide, get_random_cat_fact ]  # List of available tools

    # Binding the tools to the Model
    llm_with_tools = llm.bind_tools( tools )

    return llm_with_tools, tools
