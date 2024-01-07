from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import List, Optional

class Dish(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    img: Optional[str] = None
    is_dairy: bool
    have_nuts: bool
    breakfast_dish: bool
    lunch_dish: bool
    dinner_dish: bool
    category_id: int = 1

class Category(BaseModel):
    id: Optional[int] = None
    name: str
    img: str
    dishes: Optional[List[Dish]] = []