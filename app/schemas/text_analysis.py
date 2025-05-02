from pydantic import BaseModel, Field


class CommonWord(BaseModel):
    word: str = Field(..., description="The word")
    count: int = Field(..., description="Number of occurrences")
