from pydantic import BaseModel , root_validator
from uuid import UUID
from typing import Optional , Any

from .utils import uuid1_time_to_datetime
from app import utils

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
    created : Optional[Any] = None
    
    @root_validator(pre=True)
    def extra_create_time_from_uuid(cls, values):
        # Check if uuid exists before trying to access its time attribute
        if 'uuid' in values and values['uuid'] is not None:
            try:
                values['created'] = utils.uuid1_time_to_datetime(values['uuid'].time).timestamp()
            except (AttributeError, KeyError):
                # If there's any error accessing the time attribute, just leave created as None
                pass
        return values