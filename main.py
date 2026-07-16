from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from schemas import (
    ClassroomCreate,
    StudentCreate,
    TransferClassRequest,
    StudentResponse,
    ClassroomDetailResponse
)
from services import (
    create_classroom_service,
    create_student_service,
    get_classroom_detail_service,
    transfer_student_service
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Classroom Student API"
)

@app.post("/classrooms")
def create_classroom(
    data: ClassroomCreate,
    db: Session = Depends(get_db)
):
    return create_classroom_service(data, db)

@app.post(
    "/students",
    response_model=StudentResponse
)
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    return create_student_service(data, db)

@app.get(
    "/classrooms/{classroom_id}",
    response_model=ClassroomDetailResponse
)
def get_classroom_detail(
    classroom_id: int,
    db: Session = Depends(get_db)
):
    return get_classroom_detail_service(classroom_id, db)

@app.put(
    "/students/{student_id}/transfer",
    response_model=StudentResponse
)
def transfer_student(
    student_id: int,
    data: TransferClassRequest,
    db: Session = Depends(get_db)
):
    return transfer_student_service(student_id, data, db)
