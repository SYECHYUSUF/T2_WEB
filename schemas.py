from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nama item")
    description: Optional[str] = Field(None, description="Deskripsi item")
    price: float = Field(..., gt=0, description="Harga item (harus lebih dari 0)")
    stock: int = Field(default=0, ge=0, description="Jumlah stok item")


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int = Field(..., description="ID unik item")

    class Config:
        from_attributes = True  # Pydantic v2 (orm_mode in Pydantic v1)
