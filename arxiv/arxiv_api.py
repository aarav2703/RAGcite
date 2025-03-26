# arxiv/arxiv_api.py

import requests

BASE_ARXIV_API_URL = "http://export.arxiv.org/api/query"


def fetch_arxiv_results(query: str, start: int = 0, max_results: int = 10) -> str:
    """
    Sends a GET request to the arXiv API with the provided query.

    Parameters:
        query (str): Search query (e.g., "transformer distillation").
        start (int): Start index for pagination.
        max_results (int): Number of results to fetch.

    Returns:
        str: XML response from the arXiv API.
    """
    search_query = "+".join(query.strip().split())
    url = f"{BASE_ARXIV_API_URL}?search_query=all:{search_query}&start={start}&max_results={max_results}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"arXiv API error: {response.status_code}")

    return response.text  # Return raw Atom XML content
