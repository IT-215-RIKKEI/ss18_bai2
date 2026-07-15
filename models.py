from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    max_employees = Column(Integer, nullable=False)

    employees = relationship(
        "Employee",
        back_populates="department"
    )

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String(20), nullable=False)
    full_name = Column(String(100), nullable=False)
    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )
