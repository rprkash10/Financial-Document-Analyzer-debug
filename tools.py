import os
import json
import requests
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import BaseTool

# Tool 1: A custom Search Tool to replace SerperDevTool
class SearchTool(BaseTool):
    name: str = "Search Tool"
    description: str = "A tool for performing internet searches for recent and relevant information."

    def _run(self, query: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise ValueError("SERPER_API_KEY environment variable not set.")
            
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
        
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error performing search: {e}"

# Instantiate the search tool so we can import it elsewhere
search_tool = SearchTool()


# Tool 2: The original Financial Document Reader
class FinancialDocumentTool(BaseTool):
    name: str = "Financial Document Reader"
    description: str = "Reads the content of a financial document PDF file."

    def _run(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"Error: File not found at path {file_path}"
        
        loader = PyPDFLoader(file_path=file_path)
        pages = loader.load_and_split()
        
        full_report = ""
        for page in pages:
            full_report += page.page_content + "\n"
            
        return full_report