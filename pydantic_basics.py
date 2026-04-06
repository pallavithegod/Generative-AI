from pydantic import BaseModel

class Prod(BaseModel):
    pid : int
    price:float = 99
    in_stock:bool = True
    name:str

dict1 = {'pid' : '123', 'price' : 45.8, 'in_stock' : False, 'name' : "keyboard"}
obj1 = Prod(**dict1)       #spread
print(dict1)

obj2 = Prod(pid = 123, name = "mouse",price = 45.8)
print(obj2)


