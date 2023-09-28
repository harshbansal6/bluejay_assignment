import os

from fastapi import APIRouter, status, UploadFile, File
from app.excel.serializer.excel_s import AuthenticationResponse
from app.excel.depends.excel_d import lookup

router = APIRouter()


@router.post("/uploadfile/", response_model=AuthenticationResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)):
    # Define a directory to save the uploaded files
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save the uploaded file with a unique name
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as file_buffer:
        file_buffer.write(file.file.read())

    consecutive_days_list, time_between_shifts_list, more_than_14_hours_list = await lookup(file_path)
    response_data = {
        "message": "File uploaded successfully",
        "consecutive_days_list": consecutive_days_list,
        "time_between_shifts_list": time_between_shifts_list,
        "more_than_14_hours_list": more_than_14_hours_list
    }

    return AuthenticationResponse(**response_data)
