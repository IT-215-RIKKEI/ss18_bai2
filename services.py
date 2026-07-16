from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Classroom, Student
from schemas import ClassroomCreate, StudentCreate, TransferClassRequest

def create_classroom_service(data: ClassroomCreate, db: Session):
    classroom = Classroom(
        class_name=data.class_name,
        status=data.status,
        capacity=data.capacity
    )
    db.add(classroom)
    db.commit()
    db.refresh(classroom)

    return classroom

def create_student_service(data: StudentCreate, db: Session):
    classroom = (
        db.query(Classroom)
        .filter(Classroom.id == data.classroom_id)
        .first()
    )

    if classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )

    if classroom.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đóng"
        )

    current_count = (
        db.query(Student)
        .filter(Student.classroom_id == data.classroom_id)
        .count()
    )

    if current_count >= classroom.capacity:
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đủ sinh viên"
        )

    student = Student(
        student_code=data.student_code,
        full_name=data.full_name,
        classroom_id=data.classroom_id
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    return student

def get_classroom_detail_service(classroom_id: int, db: Session):
    classroom = (
        db.query(Classroom)
        .filter(Classroom.id == classroom_id)
        .first()
    )

    if classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )

    students = (
        db.query(Student)
        .filter(Student.classroom_id == classroom_id)
        .order_by(Student.id)
        .all()
    )

    return {
        "id": classroom.id,
        "class_name": classroom.class_name,
        "status": classroom.status,
        "capacity": classroom.capacity,
        "students": students
    }

def transfer_student_service(student_id: int, data: TransferClassRequest, db: Session):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    target_classroom = (
        db.query(Classroom)
        .filter(Classroom.id == data.new_classroom_id)
        .first()
    )

    if target_classroom is None:
        raise HTTPException(
            status_code=404,
            detail="Lớp học không tồn tại"
        )

    if target_classroom.status == "CLOSED":
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đóng"
        )

    current_count = (
        db.query(Student)
        .filter(Student.classroom_id == data.new_classroom_id)
        .count()
    )

    if current_count >= target_classroom.capacity:
        raise HTTPException(
            status_code=400,
            detail="Lớp học đã đủ sinh viên"
        )

    student.classroom_id = data.new_classroom_id
    db.commit()
    db.refresh(student)
    return student
