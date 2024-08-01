from datetime import datetime
from fastapi import Depends
from models.model_todo import Todo as TodoModel
from typing import List
from pydantic import TypeAdapter, parse_obj_as
from sqlalchemy.orm import Session
from schemas.todo_schema import TodoCreate, TodoIsDone, TodoUpdate

class RepositoryTodo:
  def __init__(self, session: Session):
        self.session = session
    
  def get_all(self, match_filter: dict, skip: int, size: int):
    owner_id = TodoModel.owner_id == match_filter["owner_id"]
    if "status" in match_filter:
        status = TodoModel.status == match_filter["status"]
        return self.session.query(TodoModel).filter(owner_id, status).offset(skip).limit(size).all()
    else :
        return self.session.query(TodoModel).filter(owner_id).offset(skip).limit(size).all()
    

  def count(self, match_filter: dict):
    owner_id = TodoModel.owner_id == match_filter["owner_id"]
    if "status" in match_filter:
        status = TodoModel.status == match_filter["status"]
        return self.session.query(TodoModel).filter(owner_id, status).count()
    else :
        return self.session.query(TodoModel).filter(owner_id).count()

  def  get_by_id(self, id: int, owner_id: int):
    return self.session.query(TodoModel).filter(TodoModel.id == id, TodoModel.owner_id == owner_id).first()
  
  def store_todo(self, data: TodoCreate):
      todo = TodoModel(
          title        = data.title,
          description  = data.description,
          status       = data.status,
          owner_id     = data.owner_id,
          created_at   = data.created_at,
          updated_at   = data.updated_at
      )
      self.session.add(todo)
      self.session.commit()
      self.session.refresh(todo)
      return todo
  
  def update(self, id: int, data: TodoUpdate, owner_id: int):
      todo = self.get_by_id(id, owner_id)
      todo.title = data.title
      todo.description = data.description
      todo.status = data.status
      todo.updated_at = datetime.now()
      self.session.commit()
      return todo
  
  def is_done(self, id: int, data: TodoIsDone, owner_id: int):
      todo = self.get_by_id(id, owner_id)
      todo.status = data.status
      todo.updated_at = datetime.now()
      self.session.commit()
      return todo
  
  def delete(self, id: int, owner_id: int):    
    todo = self.get_by_id(id, owner_id)
    self.session.delete(todo)
    self.session.commit()
    return todo
  
  # def export_list_transaction(self, match_filter: dict, projection_stage: dict):
  #   result = self.repository.find(match_filter, projection_stage)
  #   result = list(result)
  #   return result