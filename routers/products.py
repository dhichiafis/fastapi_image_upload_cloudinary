from fastapi import APIRouter,Depends,status,UploadFile,File,Form
from dotenv import load_dotenv
from models import *
from schemas import *
from database import connect
from sqlalchemy.orm import Session 
load_dotenv()
import os 

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

import json
#config = cloudinary.config(secure=True)


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


products_api=APIRouter(tags=['products'],prefix='/products')

#we store and image in cloudinary by first creating the enviroment variabl accoudng t ods
@products_api.post('/new',response_model=ProductBase)
async def create_product(
    file:UploadFile,
    title:str=Form(...),
    description:str=Form(...),
    price:float=Form(...),
        db:Session=Depends(connect)
        ):
    #reading the contents of the file and uploading them to cloudinary
    file_bytes=await file.read()
    #using cloudinary to store the file itself
    upload_result=cloudinary.uploader.upload(file_bytes,
         public_id=str(uuid.uuid4()),
         unique_filename = False, overwrite=True)
    #the url that retrieves the image
    srcURL = upload_result['secure_url']
    #we store the url in the database
    print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")
    new_product=Product(
        title=title,
        image_url=srcURL,
        price=price,
        description=description,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@products_api.get('/all',response_model=list[ProductBase])
async def get_all_products(db:Session=Depends(connect)):
    return db.query(Product).all()


@products_api.get('/{id}',response_model=ProductBase)
async def get_product(id:int,db:Session=Depends(connect)):
    return db.query(Product).filter(Product.id==id).first()