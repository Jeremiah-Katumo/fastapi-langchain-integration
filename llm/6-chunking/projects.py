from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Annotated
from pydantic import field_serializer
from datetime import date

app = FastAPI()

class User(BaseModel):
    name: str = Field(..., min_length=3)
    birth_date: date = Field(..., le=date.today())

    @computed_field
    def age(self) -> int:
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    @field_serializer('birth_date')
    def serialize_birth_date(self, birth_date: date) -> str:
        return birth_date.strftime("%Y/%m/%d")
    
@app.post("/users/")
async def create_user(user: User):
 return user.dict()