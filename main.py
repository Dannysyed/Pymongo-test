from fastapi import Depends, FastAPI, Response, status 
from fastapi.security import HTTPBearer
from utils import VerifyToken
import http.client
from db.connect import collections
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
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
    result = VerifyToken(token.credentials).verify()
    if result.get("status"):
       Response.status_code = status.HTTP_400_BAD_REQUEST
       return result
   
    print(token.credentials)
    print(name,todo)
    user_data={"name":name,"todo":todo}
    collections.insert_one(user_data)
    # mongo add data command
    note_data.append(user_data)
    print(note_data)
    return {"msg":"Succesffully added in list"}  