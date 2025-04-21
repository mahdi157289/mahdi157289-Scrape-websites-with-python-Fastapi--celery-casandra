from pydantic import BaseModel
from uuid import UUID
from typing import Optional



class ProductSchema(BaseModel):
    asin: str
    title: Optional[str]
  
  
class ProductListSchema(BaseModel):
    asin: str
    title: Optional[str]
    Price_str: Optional[str]
      
class ProductScrapeEventSchema(BaseModel):
    uuid: UUID
    asin: str
    title: Optional[str] 
class ProductScrapeEventDetailSchema(BaseModel):
    asin: str
    title: Optional[str]   