from pydantic import BaseModel
from typing import List, Optional

heirarical_model = '''
define model Address - city(str) , street(str)
define model User - name(str), address(Address) --> refererring directly to model
'''

# SELF REFERENCING / RECURRING / RECURSIVE MODEL

class Comment(BaseModel):
    id : int
    # type: int = "id"
    content : str
    replies : Optional[List['Comment']] = None   # List => Many replies at same level

Comment.model_rebuild()

comment1 = Comment(
    id = 453,
    content = "this is the first comment",
    replies = [
        Comment(id = 1453, content= "1 : first thread")
    ]
)

print(comment1)
