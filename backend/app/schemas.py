from pydantic import BaseModel
from typing import List,Optional
from datetime import datetime


class Issue(BaseModel):
    type:str
    adj:str
    noun:str
    adj_gender:Optional[str]=None
    noun_gender:Optional[str]=None
    adj_number:Optional[str]=None
    adj_number:Optional[str]=None

class TextEntryCreate(BaseModel):
    content:str
    issues: List[Issue]  # <--- важно!

class TextEntryOut(BaseModel):
    id:int 
    content:str
    issues:List[Issue]
    created_at:datetime

    class Config:
        orm_mode:True