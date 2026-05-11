import requests
from models import BookModel
from typing import List

def fetch_books(query: str) -> List[BookModel]:
    url = f"https://openlibrary.org/search.json?q={query}"
    
    try:
        response = requests.get(url)
        # Raise an exception for HTTP errors (4xx or 5xx)
        response.raise_for_status()
        data = response.json()
        
        # Convert API response docs to Pydantic models (taking first 5 results)
        books = [BookModel(**doc) for doc in data.get("docs", [])[:5]]
        return books
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

if __name__ == "__main__":
    search_term = "The Lord of the Rings"
    print(f"Searching for: {search_term}...")
    
    results = fetch_books(search_term)
    
    for book in results:
        authors = ", ".join(book.author_names) if book.author_names else "Unknown"
        print(f"- {book.title} ({book.publish_year}) by {authors}")