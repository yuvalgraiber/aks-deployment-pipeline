from pydantic import BaseModel, Field
from typing import List, Optional

class BookModel(BaseModel):
    title: str
    # Maps 'author_name' from API to 'author_names' list
    author_names: List[str] = Field(default_factory=list, alias="author_name")
    # Maps 'first_publish_year' to an optional integer
    publish_year: Optional[int] = Field(None, alias="first_publish_year")
    isbn: Optional[List[str]] = None
    key: str

    class Config:
        # Allows using aliases for population from JSON data
        populate_by_name = True