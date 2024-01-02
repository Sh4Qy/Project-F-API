from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models

def get_all(db: Session):
    categories = db.query(models.Category).all()
    return categories

def get_category(id, db: Session):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    return category

def create(request, db: Session):
    new_category = models.Category(
        name = request.name,
        img = request.img
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return f'The category {new_category.name} was added successfully'

def update(id, request, db: Session):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    category.name = request.name
    category.img = request.img
    db.commit()
    return f"The category {category.name} was successfully updated"

def delete(id, db: Session):
    category = db.query(models.Category).filter(models.Category.id == id)
    if not category.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No category found with this id: {id}")
    category_name = category.first().name
    category.delete(synchronize_session=False)
    db.commit()
    return f"The category {category_name} was successfully deleted"