"""
Concepts demonstrated:

Installing FastAPI & Uvicorn
Path operations (@app.get, @app.post, etc.)
Query parameters
Path parameters
Request & response bodies
Pydantic models
Auto-generated docs (Swagger & Redoc)

PROJECT: TO-DO LIST
"""


from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class TodoCreate(BaseModel):
    name: str

class Todo(BaseModel): # pydantic model for todo item 
    id: int
    name: str
    status: bool = False # default value
    createdAt: datetime = Field(default_factory=datetime.now) # default value is the time now
    
class TodoResponse(BaseModel):
    name: str
    createdAt: datetime


app = FastAPI()

# id generation variable
start_id: int = 101
# in-memory data store of type List[Todo]
todo_list: List[Todo] = []

@app.get("/", response_model=List[Todo]) # get route to get todo_list
def get_todo():
    return todo_list
      
@app.get("/{id}", response_model=TodoResponse) # get todo item by id 
def get_todo_id(id: int):
    for todo in todo_list:
        if todo.id == id:
            return todo
    
    return {
        "message": "invalid id"
    }
      
@app.post("/", response_model=TodoResponse) # post route to insert new todo, and response model
def post_todo(new_todo: TodoCreate):
    global start_id
    todo = Todo(id=start_id, name=new_todo.name.replace(' ', '-'))
    todo_list.append(todo)
    start_id += 1
    return todo

@app.put("/{todo_id}", response_model=TodoResponse)
def put_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            todo.status = True
            return todo
    
    return {
        "message": "id not found"
    }

# normal python function to delete completed tasks
def delete_completed():
    deleted = []
    for todo in todo_list:
        if todo.status == True:
            deleted.append(todo)
            todo_list.remove(todo)

    return deleted
        
@app.delete("/", response_model=List[TodoResponse])
def delete_todo():
    res = delete_completed()
    return res