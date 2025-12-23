from fastapi import FastAPI ,Depends,HTTPException
from routers.products import *
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware
from database import *

app=FastAPI()
Base.metadata.create_all(bind=engine)


app.include_router(products_api)
app.add_middleware(CORSMiddleware,allow_methods=[''],allow_credentials=True,allow_headers=['*'])



@app.get('/')
async def home():
    return {'message':'file handling'}


if __name__=="__main__":
    uvicorn.run('main:app',reload=True,port=9000,host='127.0.0.1')