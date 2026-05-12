import requests
import json
import sys
from models import BookModel
from typing import List

class OutputHandler:
    """
    Handles data persistence. 
    Designed as a static utility to allow for easy extension (e.g., CSV, SQL).
    """
    @staticmethod
    def save_to_json(data: List[BookModel], filename: str):
        # Convert Pydantic models to dictionaries for JSON serialization
        json_data = [book.model_dump() for book in data]
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"Data successfully saved to {filename}")

def fetch_and_process_books(query: str):
    """
    Fetches book data from Open Library API, validates via Pydantic,
    and applies business logic filters.
    """
    url = "https://openlibrary.org/search.json"
    # Using params dictionary for safe URL encoding (handles spaces/special chars)
    params = {"q": query}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    # Parse raw JSON docs into validated Pydantic models
    all_books = [BookModel(**doc) for doc in data.get("docs", [])]
    
    # FILTERING LOGIC:
    # 1. Published after 1950
    # 2. Contains 'lord' in the title (Case-insensitive)
    filtered_books = [
        book for book in all_books 
        if (book.publish_year and book.publish_year > 1950) and 
           ("lord" in book.title.lower())
    ]
    
    # Limit results to top 5 matches for cleaner output
    return filtered_books[:5]

if __name__ == "__main__":
    search_query = "The Lord of the Rings"
    
    try:
        # Fetch and process the data
        results = fetch_and_process_books(search_query)
        
        # Save results to local JSON file
        OutputHandler.save_to_json(results, "filtered_books.json")
        
    except requests.exceptions.RequestException as e:
        # Specifically handles API/Network issues
        print(f"Network error while fetching data: {e}")
        sys.exit(1) # Signals failure to Jenkins pipeline
        
    except Exception as e:
        # Catches other unexpected errors (Validation, File I/O, etc.)
        print(f"An unexpected error occurred: {e}")
        sys.exit(1) # Signals failure to Jenkins pipeline