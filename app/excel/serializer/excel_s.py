from pydantic import BaseModel
from typing import List

class EmployeeInfo(BaseModel):
    employee_name: str
    position: str

class AuthenticationResponse(BaseModel):
    message: str
    consecutive_days_list: List[EmployeeInfo]
    time_between_shifts_list: List[EmployeeInfo]
    more_than_14_hours_list: List[EmployeeInfo]
