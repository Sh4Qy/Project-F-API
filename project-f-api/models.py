from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    img = Column(String)
    
    dishes = relationship("Dish", back_populates="category")


class Dish(Base):
    __tablename__ = 'dishes'
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    img = Column(String)
    is_dairy = Column(Boolean)
    have_nuts = Column(Boolean)
    breakfast_dish = Column(Boolean)
    lunch_dish = Column(Boolean)
    dinner_dish = Column(Boolean)
    category_id = Column(Integer, ForeignKey('categories.id'))
    
    category = relationship("Category", back_populates="dishes")
    history = relationship("History", back_populates="dish")

class History(Base):
    __tablename__ ='history'

    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    time = Column(DateTime, default= datetime.now())

    dish = relationship("Dish", back_populates="history")
