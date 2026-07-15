from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Department, Employee
from schemas import EmployeeCreate

def create_employee_service(data: EmployeeCreate, db: Session) -> Employee:
    department = (
        db.query(Department)
        .filter(Department.id == data.department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Phòng ban không tồn tại"
        )

    if department.status == "INACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Phòng ban đã ngừng hoạt động"
        )

    current_count = (
        db.query(Employee)
        .filter(Employee.department_id == data.department_id)
        .count()
    )

    if current_count >= department.max_employees:
        raise HTTPException(
            status_code=400,
            detail="Phòng ban đã đủ nhân viên"
        )

    duplicate_employee = (
        db.query(Employee)
        .filter(Employee.employee_code == data.employee_code)
        .first()
    )

    if duplicate_employee:
        raise HTTPException(
            status_code=400,
            detail="Mã nhân viên đã tồn tại"
        )

    employee = Employee(
        employee_code=data.employee_code,
        full_name=data.full_name,
        department_id=data.department_id
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee
