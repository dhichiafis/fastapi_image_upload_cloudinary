from pydantic import BaseModel,ConfigDict


from datetime import datetime


class ProductCreate(BaseModel):
    title:str 
    description:str 
    price:float
    image_url:str

class ProductBase(ProductCreate):
    id:str 
    created_at:datetime
    model_config=ConfigDict(from_attributes=True)