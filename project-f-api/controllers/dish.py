from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models
import os
import random
from datetime import datetime

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
    return f"The dish {dish.name} was updated successfully"

def delete(id, db: Session):
    dish = db.query(models.Dish).filter(models.Dish.id == id)
    if not dish.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No dish found with this id: {id}")
    dish_name = dish.first().name
    dish.delete(synchronize_session=False)
    db.commit()
    return f'The dish {dish_name} was deleted successfully'

def choose_food(request, db: Session):
    dishes = db.query(models.Dish).all()
    optinal_dishes = []
    for dish in dishes:
        if request.category_id != 'All':
            if dish.category_id != int(request.category_id):
                continue
        if check_time(request, dish):
            continue
        dish_attributes = {key:attr for key,attr in vars(dish).items() if type(attr) == bool and key not in ['breakfast_dish', 'lunch_dish', 'dinner_dish']}
        choose_attributes = {key:attr for key,attr in vars(request).items() if key not in ['breakfast_dish', 'lunch_dish', 'dinner_dish', 'category_id']}
        if dish_attributes == choose_attributes:
            optinal_dishes.append(dish)
    if len(optinal_dishes) == 0:
        return 'No dish found'
    chosen_dish = random.choice(optinal_dishes)
    history = models.History(
    dish_name = chosen_dish.name,
    dish_id = chosen_dish.id
)
    db.add(history)
    db.commit()
    db.refresh(chosen_dish)
    return chosen_dish


def check_time(object, dish):
    time = int(datetime.now().strftime("%H"))
    if not object.breakfast_dish and not object.lunch_dish and not object.dinner_dish:
        if dish.breakfast_dish == True and ( 5 <= time <= 12):
            return False
        elif dish.lunch_dish == True and (12 < time <= 19):
            return False
        elif dish.dinner_dish == True and (19 < time < 5):
            return False
        else:
            return True
    dish_time = {key:value for key,value in vars(dish).items() if key in ['breakfast_dish', 'lunch_dish', 'dinner_dish']}
    for key,value in dish_time.items():
        if value == True and getattr(object, key) == True:
            return False
    return True