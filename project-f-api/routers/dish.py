from fastapi import APIRouter, Depends
from ..database import get_db
from ..controllers import dish
from .. import schemas
from typing import List

router = APIRouter(
    prefix='/dish',
    tags=["Dishes"]
)


@router.get('/', response_model=List[schemas.Dish])
def get_all(db = Depends(get_db)):
    return dish.get_all(db)

@router.get('/{id}')
def get_dish(id: int, db = Depends(get_db)):
    return dish.get_dish(id, db)

@router.post('/')
def create(request: schemas.Dish, db = Depends(get_db)):
    return dish.create(request, db)

@router.put('/{id}')
def update(id: int, request: schemas.Dish, db = Depends(get_db)):
    return dish.update(id, request, db)

@router.delete('/{id}')
def delete(id: int, db = Depends(get_db)):
    return dish.delete(id, db)