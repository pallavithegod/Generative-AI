from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Prod(BaseModel):
    pid : int
    name: str
    features: List[str]     #typing[pydantic] both used
    in_stock:bool = True
    cust_name: str = Field(
        ...,         # required field
        max_length=15,
        examples="Pallavi Jain"
    )
    image_url: Optional[str] = None    # this field may/ may not be used 

dict1 = {'pid' : '123', 'features' : ['black', 'good touch sense'], 'in_stock' : False, 'name' : "keyboard"}
obj1 = Prod(**dict1)       #spread - needs to paas each entity seperately
print(dict1)

obj2 = Prod(pid = 123, name = "mouse",features = ['good scroll', 'sleek'])
print(obj2)



