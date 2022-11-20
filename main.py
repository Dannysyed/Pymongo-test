from fastapi import Depends, FastAPI, Response, status 
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from utils import VerifyToken
import http.client
from db.connect import collections
from random import randint
app = FastAPI()    

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*",
    "http://localhost:19006"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
token_auth_bearer=HTTPBearer()
note_data=[]
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/login')
def login():
    conn = http.client.HTTPSConnection("dev-nxlrk5bn26cxoizg.us.auth0.com")

    payload = "{\"client_id\":\"xMkfJm7bNXvMjyuljJY8zU89csqDqYYf\",\"client_secret\":\"MZq1L3YPZkGIm7B3mEVFb728ShDEL2Gh8yQyuhpds7011u4dZNFoUCOnJYVx27ZA\",\"audience\":\"https://fastapi-auth0-exampled.com\",\"grant_type\":\"client_credentials\"}"

    headers = { 'content-type': "application/json" }

    conn.request("POST", "/oauth/token", payload, headers)

    res = conn.getresponse()
    data = res.read()

    return{'token':data.decode("utf-8")}



@app.post("/add_note")
def AddNote(name,todo,token:str=Depends(token_auth_bearer)):
    random_id=randint(1,10000000000)
    print(random_id)
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
       Response.status_code = status.HTTP_400_BAD_REQUEST
       return result
   
    print(token.credentials)
    # adding the data
    user_data={"id":random_id,"name":name,"todo":todo}
    collections.insert_one(user_data)
    # mongo add data command
    note_data.append(user_data)
    # showind current data
    coll=[]
    datad=collections.find({},{"_id":0})
    for data in datad:
        coll.append(data)
    print(coll)
    return {"msg":"Succesffully added in list",'newdata':coll} 


@app.get('/all_notes')
def AllNotes():
    random_id=randint(1,10000000000)
    print(random_id)
    datad=collections.find({},{"_id":0})
    coll=[]
    for data in datad:
        coll.append(data)
    print(coll)
    return{'data':coll}

@app.get('/get_note/{idd}')
def GetNote(idd):
    find_data=collections.find_one({'id':int(idd)},{'_id':0})
    return{'data':find_data}
 
@app.post('/delete_note/{idd}')
def DeleteNote(idd):
    print(idd)
    find_data=collections.find_one({'id':int(idd)},{'_id':0})
    collections.delete_one(find_data)
    print(find_data)
     # showind current data
    coll=[]
    datad=collections.find({},{"_id":0})
    for data in datad:
        coll.append(data)
    print(coll)
    return{'data':"Deleted Succesfully","newdata":coll}
        
