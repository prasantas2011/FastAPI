from sys import version
from  uuid import UUID
from xmlrpc.client import boolean
from fastapi import FastAPI, Request, Query,Depends
from pydantic import BaseModel,EmailStr
from datetime import datetime
from enum import Enum
from typing import Literal
from fastapi.responses import JSONResponse
import time

app = FastAPI()

class Role(str,Enum):
    admin = 'admin'
    user = 'user'
    guest = 'guest'

class User(BaseModel):
    id : UUID
    email: EmailStr
    date : datetime


@app.post("/item/{item_id}")
def test(item_id : int , q : str | None, item : dict[str, int],user : User,role : Role,color : Literal['red','blue'] = Query(...),in_stock : boolean = False):
    return {
        'item_id':item_id,
        'q' : q,
        'item' : item,
        'in_stock': in_stock,
        'user' : user,
        'role' :role,
        'color' :color
    }


# ---------------------------
# Custom ASGI Middleware
# ---------------------------
class CustomHeaderMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # copy headers and inject our own
            headers = list(scope["headers"])
            headers.append((b"x-customnew", b"added-by-middleware-done"))
            scope = dict(scope)
            scope["headers"] = headers

        await self.app(scope, receive, send)

# register middleware
app.add_middleware(CustomHeaderMiddleware)


# ---------------------------
# 1. Middleware (Before & After)
# ---------------------------
@app.middleware("http")
async def log_middleware(request: Request, call_next):
    start_time = time.time()
    request.state.custom_header = "added-by-middleware"

    # call the next step (routing + function)
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["test"] = 'new_test'
    return response

# ---------------------------
# 2. Dependency Injection Example
# ---------------------------
def get_custom_header(request: Request):
    custom = request.state.custom_header
    return custom

# ---------------------------
# 3. Route Handler
# ---------------------------
@app.get("/hello")
async def hello_world(request: Request ,custom_header: str = Depends(get_custom_header)):
    x =  request.state.custom_header
    customnew = request.headers.get("x-customnew")
    return {"message": "Hello World", "custom_header": custom_header, 'x' : x, 'customnew':customnew}

# ---------------------------
# 4. Custom Response Example
# ---------------------------
@app.get("/raw-response")
async def raw_response():
    return JSONResponse(content={"message": "Direct Response"}, status_code=200)
