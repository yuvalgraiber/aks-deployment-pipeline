from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class BookModel(BaseModel):
    # Pydantic v2 configuration
    model_config = ConfigDict(populate_by_name=True)

    title: str
    author_names: List[str] = Field(default_factory=list, alias="author_name")
    publish_year: Optional[int] = Field(None, alias="first_publish_year")
    isbn: Optional[List[str]] = None
    key: str