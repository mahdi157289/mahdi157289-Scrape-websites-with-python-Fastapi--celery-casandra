from pydantic import BaseModel
from uuid import UUID
from typing import Optional



class ProductSchema(BaseModel):
    asin: str
    title: Optional[str]
  
  
  
class ProductScrapeEventSchema(BaseModel):
    uuid: UUID
    asin: str
    title: Optional[str] 
  