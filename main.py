from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Department
from schemas import (
    DepartmentCreate,
    DepartmentDetailResponse,
    EmployeeCreate,
    EmployeeResponse
)
from services import create_employee_service

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Department Employee API"
)

@app.post("/departments")
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    department = Department(
        name=data.name,
        status=data.status,
        max_employees=data.max_employees
    )
    db.add(department)
    db.commit()
    db.refresh(department)

    return department

@app.get(
    "/departments/{department_id}",
    response_model=DepartmentDetailResponse
)
def get_department_detail(
    department_id: int,
    db: Session = Depends(get_db)
):
    department = (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Phòng ban không tồn tại"
        )

    return department

@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return create_employee_service(data, db)
