from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models
import os

def get_all(db: Session):
    dishes = db.query(models.Dish).all()
    return dishes

def get_dish(id, db: Session):
    dish = db.query(models.Dish).filter(models.Dish.id == id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No dish found with this id: {id}")
    return dish.category.name

def create(request ,db: Session):
    new_dish = models.Dish(
        name = request.name,
        description = request.description,
        img = request.img,
        is_dairy = request.is_dairy,
        have_nuts = request.have_nuts,
        breakfast_dish = request.breakfast_dish,
        lunch_dish = request.lunch_dish,
        dinner_dish = request.dinner_dish,
        category_id = request.category_id
    )
    db.add(new_dish)
    db.commit()
    return {'message':'Dish was created successfully', 'data': request}

async def upload(file):
    file_path = os.path.join("C:\Python FullStack\Project F\project-f\public\\uploads", file.filename)
    with open(file_path, "wb") as f:
        file_content = await file.read()
        f.write(file_content)
    return 'The file was uploaded successfully'

def update(id, request, db: Session):
    dish = db.query(models.Dish).filter(models.Dish.id == id).first()
    if not dish:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No dish found with this id: {id}")
    dish.name = request.name
    dish.description = request.description
    dish.img = request.img
    dish.is_dairy = request.is_dairy
    dish.have_nuts = request.have_nuts
    dish.breakfast_dish = request.breakfast_dish
    dish.lunch_dish = request.lunch_dish
    dish.dinner_dish = request.dinner_dish
    dish.category_id = request.category_id
    db.commit()
    return f"The dish {dish.name} was updated successfully {request}"

def delete(id, db: Session):
    dish = db.query(models.Dish).filter(models.Dish.id == id)
    if not dish.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No dish found with this id: {id}")
    dish_name = dish.first().name
    dish.delete(synchronize_session=False)
    db.commit()
    return f'The dish {dish_name} was deleted successfully'