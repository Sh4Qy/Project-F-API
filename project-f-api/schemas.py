from pydantic import BaseModel
from typing import List, Optional

class Dish(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    img: str
    is_dairy: bool
    have_nuts: bool
    breakfast_dish: bool
    lunch_dish: bool
    dinner_dish: bool
    category_id: int = 1

class Category(BaseModel):
    id: int
    name: str
    img: str
    dishes: List[Dish] = []