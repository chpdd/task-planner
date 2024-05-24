from tasks_allocation_package.classes_utils import *
from tasks_allocation_package.utils import *

if __name__ == "__main__":
    # types: better_first, better_last, mixed
    allocation_type = "better_first"
    weekends = []
    tasks_file_name = "data_files/tasks2.txt"
    days_file_name = "data_files/days2.txt"
    default_task_work_hours = 2
    default_day_work_hours = 4
    Task.set_default_work_hours(default_task_work_hours)
    Day.set_default_work_hours(default_day_work_hours)

    # get class lists
    task_pos_attr_names = ["name"]
    tasks = read_class_instances(tasks_file_name, Task, task_pos_attr_names)
    day_pos_attr_names = ["date"]
    spec_days = read_class_instances(days_file_name, Day, day_pos_attr_names)

    # print class lists
    print("Tasks:")
    task_attrs = ["name", "interest", "deadline", "work_hours"]
    print_class_instances(sorted(tasks, key=lambda tsk: tsk.interest, reverse=True),
                          *task_attrs)

    print("\nSpecial days:")
    day_attrs = ["date", "work_hours"]
    print_class_instances(sorted(spec_days, key=lambda d: d.date), *day_attrs)
    print()

    print("Calendar max_day:")
    calendar = create_calendar(tasks, spec_days)
    print(max(calendar, key=lambda d: d.date))
    print()

    print("Hours before deadline:")
    # task_name = "Java spring tutor project"
    # example_date = date.today()
    # example_deadline = next(filter(lambda t: t.name.lower() == task_name.lower(), tasks)).deadline
    example_date = date(day=1, month=1, year=2024)
    example_deadline = tasks[5].deadline
    print(get_hours_before_deadline(example_date, example_deadline, calendar))
    print()

    print("Guaranteed sort tasks:")
    sorted_tasks = guaranteed_sort(tasks)
    task_attrs = ["name", "deadline", "interest", "must_do"]
    print_class_instances(sorted_tasks, *task_attrs)
    print()

    print("Calendar with guaranteed sort tasks:")
    allocated_calendar = allocate_tasks(sorted_tasks, calendar)
    print(allocated_calendar)
