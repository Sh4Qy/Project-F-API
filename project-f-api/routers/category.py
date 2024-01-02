from fastapi import APIRouter, Depends
from ..database import get_db
from ..controllers import category
from .. import schemas
from typing import List

router = APIRouter(
    prefix='/category',
    tags=["Categories"]
)

@router.get('/', response_model=List[schemas.Category])
def get_all(db = Depends(get_db)):
    return category.get_all(db)

@router.get('/{id}')
def get_category(id, db = Depends(get_db)):
    return category.get_category(id, db)

@router.post('/')
def create(request: schemas.Category, db = Depends(get_db)):
    return category.create(request, db)

@router.put('/{id}')
def update(id, request: schemas.Category, db = Depends(get_db)):
    return category.update(id, request, db)

@router.delete('/{id}')
def delete(id , db = Depends(get_db)):
    return category.delete(id ,db)