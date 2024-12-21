from tasks_allocation_package.classes_utils import *
from tasks_allocation_package.utils import *

if __name__ == "__main__":
    """
    Name of the files from which the data is taken
    """
    tasks_file_name = "data_files/tasks3.txt"
    days_file_name = "data_files/days3.txt"

    """
    Type of task allocation
    """
    allocation_type = "better_first"

    """
    Set default working hours for all Tasks and Days
    """
    default_task_work_hours = 2
    default_day_work_hours = 4
    Task.set_default_work_hours(default_task_work_hours)
    Day.set_default_work_hours(default_day_work_hours)

    """
    Set the day from which the calendar starts
    """
    # actual_date = date.today()
    actual_date = date(day=1, month=1, year=2024)
    Task.set_actual_date(actual_date)
    Day.set_actual_date(actual_date)

    """
    Read files and write data to the Days list and the Tasks list
    """
    # get class lists
    task_pos_attr_names = ["name"]
    tasks = read_class_instances(tasks_file_name, Task, task_pos_attr_names)
    day_pos_attr_names = ["date"]
    spec_days = read_class_instances(days_file_name, Day, day_pos_attr_names)

    """
    Display Tasks and Special Days
    """
    print("Tasks")
    task_attrs = ["task_id", "name", "interest", "deadline", "work_hours"]
    print_instances(tasks, *task_attrs)
    print()

    print("Special Days")
    print(spec_days)
    print()

    """
    Display sorted list of Tasks by interest
    """
    print("Sorted tasks:")
    task_attrs = ["task_id", "name", "interest", "deadline", "work_hours"]
    print_instances(sorted(tasks, key=lambda tsk: tsk.interest, reverse=True),
                    *task_attrs)
    print()

    """
    Create calendar. A calendar is simply a list of absolutely all days from the beginning of the actual date to the maximum day.
    """
    calendar = create_calendar(tasks, spec_days)
    print("Calendar")
    print(*calendar, sep="\n")
    print("Calendar max_day:")
    print(max(calendar, key=lambda d: d.date))
    print(f"Days in calendar={len(calendar)}")
    print()

    """
    Sorting in which all mandatory tasks have first priority
    """
    print("Must_do sort tasks:")
    sorted_tasks = deadline_mustdo_sort(tasks)
    task_attrs = ["name", "deadline", "interest", "must_do"]
    print_instances(sorted_tasks, *task_attrs)
    print()

    print("Calendar with must_do sort tasks:")
    guar_allocated_calendar = allocate_tasks(sorted_tasks, calendar)
    # print(*filter(lambda day_: day_.has_tasks(), allocated_calendar), sep="\n")
    print_calendar_with_schedule_rus(guar_allocated_calendar, tasks)

    print("Failed tasks:")
    failed_task_ids = validate_allocation(guar_allocated_calendar, tasks)
    failed_tasks = []
    for task_id_ in failed_task_ids:
        failed_tasks.append(get_instance_by_attr(tasks, "task_id", task_id_))
    print_instances(failed_tasks, *task_attrs)
    print(f"Is it possible to complete all the must_do tasks: {not contains_must_do(failed_tasks)}")
    print()

    """
    Smart task sorting
    """
    print("Smart sort:")
    smart_sorted_work_hours = smart_sort_v2(tasks, calendar)
    print(f"smart_sorted_work_hours: {smart_sorted_work_hours}")
    smart_sorted_calendar = allocate_work_hours(smart_sorted_work_hours, calendar)
    print_calendar_with_schedule_rus(smart_sorted_calendar, tasks)
    # print(*smart_sorted_calendar, sep="\n")