from datetime import datetime, timezone
from typing import Literal, Optional
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from ..auth.jwt_handler import create_access_token
from ..database import get_db
from ..model import employee, department
from ..auth.jwt_handler import create_access_token , verify_access_token

router = APIRouter(prefix="/register", tags=["register"])



















class registerRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    phone_number: str = Field(min_length=10, max_length=15)
    designation: str = Field(min_length=2, max_length=100)
    department_id: int
    manager_id: Optional[int] = None
    joining_date: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    role: Literal["Admin", "Manager", "Employee", "HR"] = "Employee"


class departmentRequest(BaseModel):
    department_name: str = Field(min_length=2, max_length=100)


class loginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def user_to_dict(emp: employee) -> dict:
    return {
        "id": emp.id,
        "full_name": emp.full_name,
        "email": emp.email,
        "phone_number": emp.phone_number,
        "designation": emp.designation,
        "role": emp.role,
        "department_id": emp.department_id,
        "employee_status": emp.employee_status,
        "joining_date": emp.joining_date.isoformat() if emp.joining_date else None,
    }


@router.post("/create", status_code=201)
def register_employee(request: registerRequest, db: Session = Depends(get_db)):
    existing_employee = db.query(employee).filter(
        (employee.email == request.email) | (employee.phone_number == request.phone_number)
    ).first()
    if existing_employee:
        raise HTTPException(status_code=400, detail="Email or phone number already exists")

    dept = db.query(department).filter(department.id == request.department_id).first()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")

    new_employee = employee(
        full_name=request.full_name,
        email=request.email,
        hashed_password=hash_password(request.password),
        phone_number=request.phone_number,
        designation=request.designation,
        department_id=request.department_id,
        manager_id=request.manager_id,
        joining_date=request.joining_date,
        role=request.role,
        employee_status="Active",
        is_active=True,
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    access_token = create_access_token(
        employee_id=new_employee.id,
        role=new_employee.role,
        email=new_employee.email,
        full_name=new_employee.full_name,
    )

    return {
        "message": "Employee registered successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_to_dict(new_employee),
    }


@router.post("/login", status_code=200)
def login_employee(request: loginRequest, db: Session = Depends(get_db)):
    employee_check = db.query(employee).filter(employee.email == request.email).first()
    if not employee_check:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not bcrypt.checkpw(request.password.encode(), employee_check.hashed_password.encode()):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(
        employee_id=employee_check.id,
        role=employee_check.role,
        email=employee_check.email,
        full_name=employee_check.full_name,
    )

    return {
        "message": "Sign-in successful!",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_to_dict(employee_check),
    }


@router.post("/create_department", status_code=201)
def create_department(request: departmentRequest, db: Session = Depends(get_db)):
    existing_department = db.query(department).filter(
        department.department_name == request.department_name
    ).first()
    if existing_department:
        raise HTTPException(status_code=400, detail="Department name already exists")

    new_department = department(department_name=request.department_name)

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return {
        "message": "Department created successfully",
        "department": {
            "id": new_department.id,
            "department_name": new_department.department_name,
        },
    }