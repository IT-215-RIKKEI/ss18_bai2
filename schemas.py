from typing import List
from pydantic import BaseModel, ConfigDict, Field

class DepartmentCreate(BaseModel):
    name: str
    status: str
    max_employees: int

class EmployeeCreate(BaseModel):
    employee_code: str
    full_name: str
    department_id: int

class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    full_name: str
    department_id: int
    model_config = ConfigDict(from_attributes=True)

class DepartmentDetailResponse(BaseModel):
    id: int
    name: str
    status: str
    max_employees: int
    employees: List[EmployeeResponse] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)
