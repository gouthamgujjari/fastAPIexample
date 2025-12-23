
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
