from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_employee
from ..database import get_db
from ..model import employee

router = APIRouter(prefix="/admin", tags=["admin"])


class AdminRole(BaseModel):
    role: str = Field(min_length=2, max_length=50)


class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str
    designation: str
    joining_date: datetime
    role: str
    employee_status: str
    department_id: int
    manager_id: Optional[int] = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[EmployeeResponse], status_code=200)
def get_all_employees(
    db: Session = Depends(get_db),
    current_employee: employee = Depends(get_current_employee),
):
    if current_employee.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    return db.query(employee).all()