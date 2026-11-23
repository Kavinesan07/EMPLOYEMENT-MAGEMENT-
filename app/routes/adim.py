import os
from urllib import request
import bcrypt
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_employee
from ..auth.jwt_handler import create_access_token , verify_access_token
from ..database import get_db
from ..model import employee, department



router = APIRouter(prefix="/adim", tags=["adim"])

class adimrole (BaseModel):
    role: str = Field(min_length=2, max_length=50)




@router.get("/" ,response_model=list[employee],status_code=200)
def get_all_employees( db: Session = Depends(get_db), current_employee: employee = Depends(get_current_employee)):
    employees = db.query(employee).all()
    return employees