import requests
import json
import sys
import os
from models import BookModel
from typing import List

# Safe parsing with fallback
try:
    TIMEOUT_VAL = int(os.getenv("HTTP_TIMEOUT", "30"))
except ValueError:
    TIMEOUT_VAL = 30

SEARCH_QUERY = os.getenv("SEARCH_QUERY", "The Lord of the Rings")
API_URL = os.getenv("API_URL", "https://openlibrary.org/search.json")
FILTER_KEYWORD = os.getenv("FILTER_KEYWORD", "lord")


class OutputHandler:
    @staticmethod
    def save_to_json(data: List[BookModel], filename: str):
        json_data = [book.model_dump() for book in data]
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=4)
        print(f"Data successfully saved to {filename}")


def fetch_and_process_books(query: str):
    params = {"q": query}
    headers = {"User-Agent": "DevOpsTask-BookFetcher/1.0"}

    response = requests.get(
        API_URL,
        params=params,
        headers=headers,
        timeout=TIMEOUT_VAL
    )
    response.raise_for_status()
    data = response.json()

    all_books = [BookModel(**doc) for doc in data.get("docs", [])]

    filtered_books = [
        book for book in all_books
        if (book.publish_year and book.publish_year > 1950) and
           (FILTER_KEYWORD in book.title.lower())
    ]

    return filtered_books[:5]


if __name__ == "__main__":
    try:
        results = fetch_and_process_books(SEARCH_QUERY)
        OutputHandler.save_to_json(results, "filtered_books.json")
    except requests.exceptions.Timeout:
        print(f"Error: The request timed out after {TIMEOUT_VAL} seconds.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)