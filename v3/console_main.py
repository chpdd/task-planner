from tasks_allocation_package.classes_utils import *
from tasks_allocation_package.utils import *

if __name__ == "__main__":
    tasks_file_name = "tasks.txt"
    days_file_name = "days.txt"

    default_task_work_hours = 2
    default_day_work_hours = 4
    Task.set_default_work_hours(default_task_work_hours)
    Day.set_default_work_hours(default_day_work_hours)

    # actual_date = date.today()
    actual_date = date(day=1, month=1, year=2024)
    Task.set_actual_date(actual_date)
    Day.set_actual_date(actual_date)

    task_positional_attr_names = ["name"]
    tasks = read_class_instances(tasks_file_name, Task, task_positional_attr_names)
    day_pos_attr_names = ["date"]
    spec_days = read_class_instances(days_file_name, Day, day_pos_attr_names)

    print("Задачи:")
    print_present_tasks_rus(tasks)
    print()

    calendar = create_calendar(tasks, spec_days)
    print(calendar)
    smart_sorted_work_hours = smart_sort_v1(tasks, calendar)
    print(smart_sorted_work_hours)
    smart_sorted_calendar = allocate_work_hours(smart_sorted_work_hours, calendar)
    print(smart_sorted_calendar)
    print_calendar_with_schedule_rus(smart_sorted_calendar, tasks)
