from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional

class Prod(BaseModel):   # PROD IS A MODEL
    pid : int
    name: str

    features: List[str]     #typing[pydantic] both used
    in_stock:bool = True

    cust_name: str = Field(
        ...,         # required field
        max_length=15,
        examples="Pallavi Jain"
    )

    price : float    # $5,600
    @field_validator('price', mode= 'before')          # for validation
    def parse_price(cls, v):
        if isinstance(v, str):       # to check if an object belongs to a specific class/ data type/ tuple of types
            result = float(v.replace('$', '').replace(',', ''))
            return result
        return v

    image_url: Optional[str] = None    # this field may/ may not be used 


dict1 = {'cust_name' : "pallavi", 'pid' : '123', 'features' : ['black', 'good touch sense'], 'in_stock' : False, 'name' : "keyboard", 'price' : '500'}
obj1 = Prod(**dict1)       #spread - needs to paas each entity seperately
print(dict1)

obj2 = Prod(cust_name= "pallavithegod" ,pid = 123, name = "mouse",price = '$ 5,600', features = ['good scroll', 'sleek'])
print(obj2.model_dump())



