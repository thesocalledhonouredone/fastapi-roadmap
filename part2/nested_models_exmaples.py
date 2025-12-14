from pydantic import BaseModel
from typing import List, Optional

# eg 1: Simple Nested Model
class Address(BaseModel):
    street: str
    city: str
    zip_code: int

class User(BaseModel):
    name: str
    age: int
    address: Address # using Address model as a nested model



# eg 2: Nested Lists Model
class Item(BaseModel):
    name: str
    price: str

class Order(BaseModel):
    order_id: int
    items: List[Item] # a list of Item models



# eg 3: Deeply Nested Models
class Engine(BaseModel):
    hp: int

class Car(BaseModel):
    make: str
    model: str
    engine: Engine

class Garage(BaseModel):
    cars: List[Car]



# eg 4: Optional Nested Models
class Disability(BaseModel):
    condition: str

class Customer(BaseModel):
    name: str
    age: int
    email: str
    special_able: Optional[Disability] = None
