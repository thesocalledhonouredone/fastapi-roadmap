from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field, HttpUrl # type of url 
from datetime import datetime
from typing import Dict, List

# basic model for url-shorner that user sends
class UrlCreate(BaseModel):
    original_url : HttpUrl

# basic model for url-shortner
class Url(BaseModel):
    original_url: HttpUrl
    short_code: str
    createdAt: datetime = Field(default_factory=datetime.now)

# random string short-code generation logic
import random
import string

chars_string = string.ascii_letters + string.digits

def generate_random_string(length: int = 6) -> str:
    random_string = ""
    for i in range(length):
        random_string += random.choice(chars_string)
    return random_string
# print(generate_random_string())


# in-memory store for urls
url_db: Dict[str, Url] = { # [str-key(short-code), Url-value(original url)]
    
}

# fastapi app initlization
app = FastAPI()

@app.get("/")
def home_page():
    return {
        "page": "URL-SHORTNER"
    }
    
@app.get("/api/urls", response_model=List[Url]) # get all urls
def get_urls():
    return list(url_db.values())

@app.get("/api/urls/{short_code}") # get route to short-code url
def get_url_by_short_code(short_code: str):
    url = url_db.get(short_code)
    if not url:
        return { "message": "short code not valid" }

    return RedirectResponse(url.original_url) # redirect to the corresponding original url

@app.post("/api/urls") # post new url
def post_url(new_url: UrlCreate):
    short_code = generate_random_string()
    while short_code in url_db:
        short_code = generate_random_string()
        
    url = Url(
        original_url = new_url.original_url,
        short_code = short_code
    )
    
    url_db[short_code] = url
    return url
