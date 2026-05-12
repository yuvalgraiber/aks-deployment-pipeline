import requests
import json
import sys
from models import BookModel
from typing import List

class OutputHandler:
    @staticmethod
    def save_to_json(data: List[BookModel], filename: str):
        json_data = [book.model_dump() for book in data]
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"Data successfully saved to {filename}")

def fetch_and_process_books(query: str):
    url = "https://openlibrary.org/search.json"
    params = {"q": query}
    headers = {"User-Agent": "DevOpsTask-BookFetcher/1.0"}
    
    # Added timeout for production reliability
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    all_books = [BookModel(**doc) for doc in data.get("docs", [])]
    
    filtered_books = [
        book for book in all_books 
        if (book.publish_year and book.publish_year > 1950) and 
           ("lord" in book.title.lower())
    ]
    
    return filtered_books[:5]

if __name__ == "__main__":
    search_query = "The Lord of the Rings"
    
    try:
        results = fetch_and_process_books(search_query)
        OutputHandler.save_to_json(results, "filtered_books.json")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)