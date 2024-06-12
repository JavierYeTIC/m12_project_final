import datetime
from pydantic import BaseModel, SkipValidation

class Product(BaseModel):
    product_id: int 
    name: str
    img: str
    description: str
    company: str
    price: float
    units: int
    subcategory_id: int
    created_at: SkipValidation[datetime.datetime]
    updated_at: SkipValidation[datetime.datetime]

    class Config:
        arbitrary_types_allowed = True
