from pydantic import BaseModel
from typing import List


class AuthenticationResponse(BaseModel):
    message: str
    consecutive_days_list: List[str]
    time_between_shifts_list: List[str]
    more_than_14_hours_list: List[str]
