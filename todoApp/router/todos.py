from pathlib import Path
from fastapi import HTTPException
from .auth import get_current_user
from fastapi import FastAPI,Depends,APIRouter,HTTPException
from starlette import status
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todos
from pydantic import BaseModel,Field


router=APIRouter()




def get_db():
    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()



db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

class TodoRequest(BaseModel):
    title: str=Field(min_length=3)
    description: str=Field(min_length=3,max_length=100)
    priority: int=Field(gt=0,lt=6)
    complete: bool



@router.get("/")
async def real_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Dsad")
    return db.query(Todos).filter(Todos.owner_id==user.get("id")).all()



@router.get("/todo/{todo_id}")
async def read_todo(user: user_dependency,todo_id: int, db: db_dependency):

    if user is None:
        raise HTTPException(status_code=401,detail="fail")

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found")

@router.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,db: db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="fail")
    todo_model=Todos(**todo_request.dict(),owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()



@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency,db: db_dependency,todo_request: TodoRequest,todo_id: int=Path(gt=0)):
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()


    if todo_model is None:
        raise HTTPException(status_code=404,detail="dsadad")

    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency,db: db_dependency,todo_id: int=Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401,detail="dsadsad")

    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="todo not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()

    db.commit()





