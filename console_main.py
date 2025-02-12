from tasks_allocation_package.classes import Planner

import datetime as dt
import os.path

if __name__ == "__main__":
    tasks_file_name = os.path.join("data_files", "tasks7.txt")
    days_file_name = os.path.join("data_files", "days7.txt")

    default_task_work_hours = 2
    default_day_work_hours = 4

    start_date = dt.date.today()
    tasks = Planner.read_tasks_from_file(tasks_file_name, default_task_work_hours)
    days = Planner.read_days_from_file(days_file_name, default_day_work_hours)
    planner = Planner(tasks, days, start_date=start_date, dflt_day_work_hours=default_day_work_hours,
                         dflt_task_work_hours=default_task_work_hours)

    # planner.interest_importance_sort()
    planner.print_present_tasks_rus()
    planner.force_procrastinate_sort()
    planner.print_failed_tasks_rus()
    planner.print_calendar_with_schedule_rus()
