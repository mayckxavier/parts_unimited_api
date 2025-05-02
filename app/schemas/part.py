from pydantic import BaseModel, Field, validator
from typing import Optional


# Base Part schema with common attributes
class PartBase(BaseModel):
    name: str = Field(..., max_length=150, description="Name of the part")
    sku: str = Field(..., max_length=30, description="Stock Keeping Unit identifier")
    description: Optional[str] = Field(None, max_length=1024, description="Description of the part")
    weight_ounces: Optional[int] = Field(None, ge=0, description="Weight in ounces")
    is_active: bool = Field(True, description="Whether the part is active")

    @validator('sku')
    def sku_valid_format(cls, v):
        if not v or len(v) < 5:
            raise ValueError("SKU must be at least 5 characters long")
        return v


# Schema for creating a new Part
class PartCreate(PartBase):
    pass


# Schema for updating a Part
class PartUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=150)
    sku: Optional[str] = Field(None, max_length=30)
    description: Optional[str] = Field(None, max_length=1024)
    weight_ounces: Optional[int] = None
    is_active: Optional[bool] = None


# Schema for returning a Part from the API
class Part(PartBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


# Schema for pagination
class PartList(BaseModel):
    items: list[Part]
    total: int
    page: int
    page_size: int
    pages: int
