from sqlalchemy import Column,Integer,ForeignKey,String,Float,DateTime
from database import *
from datetime import datetime
import uuid
class Product(Base):
    __tablename__='products'
    id=Column('id',String,primary_key=True,
              default=lambda:str(uuid.uuid4()))#we are using uuid4 by converting it into string
    title=Column('title',String,unique=True)
    description=Column('description',String)
    image_url=Column('image_url',String)
    price=Column('price',Float)
    created_at=Column('created_at',DateTime,default=datetime.now)


