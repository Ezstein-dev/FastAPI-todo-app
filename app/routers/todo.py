from fastapi import HTTPException, APIRouter, Response, status, Depends
from typing import List
from app import models,oauth2
from app.database import get_db
from .. import schemas
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/todo",
    tags=['Todo']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoIn, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    todo_dict = models.Todo(owner_id = current_user.id, **todo.dict())
    db.add(todo_dict)
    db.commit()
    db.refresh(todo_dict)
    return todo_dict


@router.get("/", response_model=List[schemas.Todo])
def get_all_todo(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    todo = db.query(models.Todo).all()
    return todo


@router.get("/{id}")
def get_one_todo(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    todo = db.query(models.Todo).filter(models.Todo.id == id).first()
    try:
        return todo
    except:
        raise HTTPException(status_code=404, detail=f"Todo with the id: {id} does not exist")


@router.put("/{id}", response_model=schemas.Todo)
def update_todo(id: int, updated_todo: schemas.TodoIn, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    todo = todo_query.first()
    if todo == None:
        raise HTTPException(status_code=404, detail=f"Todo with the id: {id} does not exist")
    todo_query.update(updated_todo.dict(), synchronize_session=False)
    db.commit()
    return todo


@router.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    todo_query = db.query(models.Todo).filter(models.Todo.id == id)
    todo = todo_query.first()
    if todo == None:
        raise HTTPException(status_code=404, detail=f"Todo with the id: {id} does not exist")
    todo_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
