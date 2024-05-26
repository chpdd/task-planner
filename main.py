from tasks_allocation_package.classes_utils import *
from tasks_allocation_package.utils import *

if __name__ == "__main__":
    tasks_file_name = "data_files/tasks.txt"
    days_file_name = "data_files/days.txt"

    allocation_type = "better_first"

    default_task_work_hours = 2
    default_day_work_hours = 6
    Task.set_default_work_hours(default_task_work_hours)
    Day.set_default_work_hours(default_day_work_hours)

    actual_date = date.today()
    Task.set_actual_date(actual_date)
    Day.set_actual_date(actual_date)

    # get class lists
    task_pos_attr_names = ["name"]
    tasks = read_class_instances(tasks_file_name, Task, task_pos_attr_names)
    day_pos_attr_names = ["date"]
    spec_days = read_class_instances(days_file_name, Day, day_pos_attr_names)

    # print class lists
    print("Tasks:")
    task_attrs = ["task_id", "name", "interest", "deadline", "work_hours"]
    print_instances(sorted(tasks, key=lambda tsk: tsk.interest, reverse=True),
                    *task_attrs)
    print()

    print("Special days:")
    day_attrs = ["date", "work_hours"]
    print_instances(sorted(spec_days, key=lambda d: d.date), *day_attrs)
    print()

    print("Calendar max_day:")
    calendar = create_calendar(tasks, spec_days)
    print(max(calendar, key=lambda d: d.date))
    print(f"Days in calendar={len(calendar)}")
    print()

    print("Work hours before deadline:")
    # task_name = "Java spring tutor project"
    # example_date = date.today()
    # example_deadline = next(filter(lambda t: t.name.lower() == task_name.lower(), tasks)).deadline
    example_date = date.today()
    example_deadline = tasks[5].deadline
    print(get_hours_before_deadline(example_date, example_deadline, calendar))
    print()

    print("Guaranteed sort tasks:")
    sorted_tasks = deadline_mustdo_sort(tasks)
    task_attrs = ["name", "deadline", "interest", "must_do"]
    print_instances(sorted_tasks, *task_attrs)
    print()

    print("Calendar with guaranteed sort tasks:")
    allocated_calendar = allocate_tasks(sorted_tasks, calendar)
    # print(*filter(lambda day_: day_.has_tasks(), allocated_calendar), sep="\n")
    print_calendar_with_schedule(allocated_calendar, tasks)

    print("Failed tasks:")
    failed_task_ids = validate_allocation(allocated_calendar, tasks)
    failed_tasks = []
    for task_id_ in failed_task_ids:
        failed_tasks.append(get_instance_by_attr(tasks, "task_id", task_id_))
    print_instances(failed_tasks, *task_attrs)
    print(f"Is it possible to complete all the must_do tasks: {not contains_must_do(failed_tasks)}")
