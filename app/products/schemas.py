from typing import List, Optional
from pydantic import BaseModel, HttpUrl, conint
from enum import Enum

class ProductCondition(str, Enum):
    brand_new = "brand-new"
    mint_condition = "mint condition"
    like_new = "like-new"
    excellent = "excellent"
    good = "good"
    fair = "fair"

class ProductDimension(BaseModel):
    width: float
    height: float
    length: float
    weight: float

class SellerInfo(BaseModel):
    full_name: str 

class ProductSchema(BaseModel):
    id: int
    images: List[HttpUrl]
    category: str
    title: str
    description: str
    condition: ProductCondition
    price: float
    dimensions_width: float
    dimensions_height: float
    dimensions_length: float
    dimensions_weight: float
    brand: Optional[str] = None
    material: Optional[str] = None
    stock: conint(ge=1)
    sku: str
    tags: List[str] = []
    seller: SellerInfo

    class Config:
        orm_mode = True
