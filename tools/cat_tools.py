# This tool fetches random cat facts from an external API.

import requests
from langchain_core.tools import tool

@tool
def get_random_cat_fact() -> str:
    """
        Retrieves a random fact about cats from the Cat Fact API.
        Use this tool whenever the user asks for curiosity, facts, or information about cats.
        This tool takes no arguments.
        This is your final answer when the user requests a cat fact.
    """
    try:

        # A URL foi retirada da documentação que você enviou
        url = "https://catfact.ninja/fact"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('fact', "No fact found.")
        
        else:
            return f"ERROR: API returned status code {response.status_code}"
            
    except Exception as e:
        return f"ERROR: Connecting to Cat API: {str(e)}"
    
# The API documentation is here:
# https://catfact.ninja/