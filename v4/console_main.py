from tasks_allocation_package.classes import Planner

import datetime as dt
import os.path

if __name__ == "__main__":
    tasks_file_name = os.path.join("data_files", "tasks2.txt")
    days_file_name = os.path.join("data_files", "days2.txt")

    default_task_work_hours = 2
    default_day_work_hours = 4

    start_date = dt.date(day=1, month=1, year=2024)
    tasks = Planner.get_tasks_from_file(tasks_file_name)
    # print(*tasks, sep="\n")
    manual_days = Planner.get_days_from_file(days_file_name)
    planner = Planner(tasks=tasks, manual_days=manual_days, start_date=start_date,
                      dflt_day_work_hours=default_day_work_hours, dflt_task_work_hours=default_task_work_hours)
    planner.simple_sort()
    planner.validate_allocation()
    planner.print_failed_tasks()
    planner.print_calendar_with_schedule_rus()

