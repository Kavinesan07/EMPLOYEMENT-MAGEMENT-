import os
from urllib import request
import bcrypt
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..model import employee, department


router = APIRouter(prefix="/register", tags=["register"])

class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(min_length=2, max_length=100)
    phone_number: str = Field(min_length=10, max_length=15)
    designation: str = Field(min_length=2, max_length=100)
    joining_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    role: str = Field(min_length=2, max_length=50)


    
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

class departmentRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr = Field(min_length=2, max_length=100)
    department_name: str = Field(min_length=2, max_length=100)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)



def user_to_dict(employee: employee) -> dict:
    return {
        "id": employee.id,
        "username": employee.username,
        "email": employee.email,
        "role": getattr(employee, "role", 0) if getattr(employee, "role", 0) is not None else 0,
        "created_at": employee.created_at.isoformat() if employee.created_at else None,
        "updated_at": employee.updated_at.isoformat() if employee.updated_at else None,
    }


@router.post("/create" ,status_code=201)

def register_employee(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if the email or phone number already exists
    existing_employee = db.query(employee).filter(
        (employee.email == request.email) | (employee.phone_number == request.phone_number)
    ).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Email or phone number already exists")

    # Create a new employee instance
    new_employee = employee(
        full_name=request.full_name,
        email=request.email,
        phone_number=request.phone_number,
        designation=request.designation,
        joining_date=request.joining_date,
        role=request.role,
        employee_status="Active",
        is_active=True
    )

    # Add the new employee to the database
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return {"message": "Employee registered successfully", "employee": user_to_dict(new_employee)}

@router.post("/login", status_code=200)

def login_employee(request: LoginRequest, db: Session = Depends(get_db)):
    # Check if the email exists
    employee_record = db.query(employee).filter(employee.email == request.email).first()
    if not employee_record:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    if not bcrypt.checkpw(request.password.encode(), employee_record.hashed_password.encode()):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful", "employee": user_to_dict(employee_record)}


@router.post("/create_department", status_code=201)
def create_department(request: departmentRequest, db: Session = Depends(get_db)):
    # Check if the department name already exists
    existing_department = db.query(department).filter(department.department_name == request.department_name).first()
    if existing_department:
        raise HTTPException(status_code=400, detail="Department name already exists")

    # Create a new department instance
    new_department = department(
        department_name=request.department_name
    )

    # Add the new department to the database
    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return {"message": "Department created successfully", "department": {"id": new_department.id, "department_name": new_department.department_name}}