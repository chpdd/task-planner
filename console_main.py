from tasks_planner import Planner

import datetime as dt
import os

if __name__ == "__main__":
    tasks_file_name = os.path.join("data_files", "tasks8.txt")
    days_file_name = os.path.join("data_files", "days8.txt")

    default_task_work_hours = 2
    default_day_work_hours = 4

    start_date = dt.date(day=1, month=1, year=2025)
    # start_date = dt.date.today()
    tasks = Planner.read_tasks_from_file(tasks_file_name, default_task_work_hours)
    days = Planner.read_days_from_file(days_file_name, default_day_work_hours)
    planner = Planner(tasks, days, start_date=start_date, dflt_day_work_hours=default_day_work_hours,
                      dflt_task_work_hours=default_task_work_hours)

    print(planner.tasks_str_table_rus(planner.tasks, "Таблица задач"))
    allocation_types = [
        (Planner.importance_allocation, "Распределение по важности"),
        (Planner.interest_allocation, "Распределение по интересу"),
        (Planner.interest_importance_allocation, "Распределение по важности умноженной на интерес"),
        (Planner.points_allocation, "Распределение по важности, умноженной на часы"),
        (Planner.force_procrastinate_allocation, 'Распределение "принудительная прокрастинация"'),
    ]
    print("Виды распределений:")
    for i in range(len(allocation_types)):
        print(f"{i + 1}. {allocation_types[i][1]}")
    print("Напишите номер распределения, которое хотите применить: ", end="")
    k = input()
    while not k.isdigit() or not (0 < int(k) <= len(allocation_types)):
        print(f"Введённое значение должно быть числом от 1 до {len(allocation_types)}")
        k = input()
    k = int(k) - 1
    allocation_types[k][0](planner)

    result_file_name = "planner_result.txt"
    print()
    print(planner.failed_tasks_str_table_rus())
    print(planner.calendar_str_tables_rus(), end="")
    planner.write_result_to_file(result_file_name, allocation_types[k][1])
