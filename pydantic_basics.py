from pydantic import BaseModel, Field, field_validator, field_serializer
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import ConfigDict

class Prod(BaseModel):   # PROD IS A MODEL - 8 fields
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
 
    added_at: datetime
    # changes 2026-04-09T21:40:10 to more human readable form
    @field_serializer('added_at')
    def export_dt(self, datetime):
        return datetime.strftime('%d-%m-%y %H:%M:%S')

    # OBSOLETE
    # model_config = ConfigDict(
    #     json_encoders= {datetime: lambda v: v.strftime('%d-%m-%y %H:%M:%S')}
    #     # json_encoders => Use above logic on every datetime object during JSON conversion(not default format)
    # )


dict1 = {'cust_name' : "pallavi", 'pid' : '123', 'added_at': datetime(2013,4,2), 'features' : ['black', 'good touch sense'], 'in_stock' : False, 'name' : "keyboard", 'price' : '500'}
obj1 = Prod(**dict1)       #spread - needs to paas each entity seperately
print(dict1)
print("=" * 100)

obj2 = Prod(cust_name= "pallavithegod" ,pid = 123, name = "mouse",price = '$ 5,600', features = ['good scroll', 'sleek'], added_at= datetime(2016,2,29,6,6,59))
print(obj2.model_dump())

#Serialised
print("=" * 100)
print(obj2.model_dump_json())



