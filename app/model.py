from app.database import Base 
from app.database import engine
from sqlalchemy import CheckConstraint, Column, DateTime, Float, Index, Integer, String, Text, text, Boolean,ForeignKey, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime , timedelta , timezone 
from pydantic import BaseModel









def utc_now():
    return datetime.now(timezone.utc)

class employee(Base):
    __tablename__ = "employee"

    __table_args__ = (CheckConstraint("employee_status IN ('Active', 'Inactive')", name="employee_status_check"),)

    __table_args__ = (CheckConstraint("role IN ('Admin', 'Manager', 'Employee', 'HR')", name="role_check"),)

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), primary_key=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    designation = Column(String(100), nullable=False)
    joining_date = Column(DateTime, nullable=False, default=utc_now)
    role = Column(String(50), nullable=False, default="Employee")
    employee_status = Column(String(50), nullable=False, default="Active")
    department_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("employee.id"), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)





    class department(Base):
        __tablename__ = "department"
        id = Column(Integer, primary_key=True, index=True)
        department_name = Column(String(100), unique=True, nullable=False)





        
