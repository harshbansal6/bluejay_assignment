import pandas as pd
from datetime import timedelta

from app.excel.serializer.excel_s import EmployeeInfo


async def lookup(file):
    df = pd.read_excel(file)

    df["Time"] = pd.to_datetime(df["Time"])
    df["Time Out"] = pd.to_datetime(df["Time Out"])
    # Group records by Employee Name
    grouped = df.groupby("Employee Name")

    # Initialize lists to store employees who meet the criteria
    consecutive_days_list = []
    time_between_shifts_list = []
    more_than_14_hours_list = []

    for employee_name, group in grouped:
        consecutive_days_count = 0
        time_between_shifts = timedelta()
        max_single_shift_hours = 0
        position = None  # Initialize position to None

        for index, row in group.iterrows():
            if row["Position Status"] == "Active":
                if consecutive_days_count == 0:
                    start_time = row["Time"]
                    end_time = row["Time Out"]
                    max_single_shift_hours = max(max_single_shift_hours, (end_time - start_time).total_seconds() / 3600)
                else:
                    end_time = row["Time Out"]
                    time_between_shifts += start_time - previous_end_time
                    max_single_shift_hours = max(max_single_shift_hours, (end_time - start_time).total_seconds() / 3600)

                if time_between_shifts.total_seconds() / 3600 > 1:
                    consecutive_days_count = 0

                if (end_time - start_time).total_seconds() / 3600 > 14:
                    more_than_14_hours_list.append(EmployeeInfo(employee_name=employee_name, position=position))

                start_time = row["Time"]
                previous_end_time = row["Time Out"]
                consecutive_days_count += 1
                position = row["Position ID"]  # Store the current position

                if consecutive_days_count >= 7:
                    consecutive_days_list.append(EmployeeInfo(employee_name=employee_name, position=position))

                if ( time_between_shifts.total_seconds() / 3600 < 10 and
                        time_between_shifts.total_seconds() / 3600 > 1 ):
                    time_between_shifts_list.append(EmployeeInfo(employee_name=employee_name, position=position))

    print(consecutive_days_list)
    return consecutive_days_list, time_between_shifts_list, more_than_14_hours_list
