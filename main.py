from datetime import timedelta, datetime, date

from Task import Task, TooDistantDateError
from Day import Day


def print_class_objs(input_list: [], *attrs):
    for elem in input_list:
        for attr in attrs:
            result = getattr(elem, attr, "No attr")
            if isinstance(result, datetime):
                result = result.date()
            print(f"{attr}={result}", end=", ")
        print()


def read_class_objs(file_name: str, class_init, *pos_attr_names: []) -> []:
    result = []
    with open(file_name, 'r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            attrs = line.strip().split(",")
            kw_attrs = dict()
            pos_attrs = []
            for i in range(len(attrs)):
                attr_str = attrs[i].strip()
                if i < len(pos_attr_names):
                    pos_attrs.append(attr_str)
                elif ":" in attr_str:
                    key, val = attr_str.split(":")
                    kw_attrs[key.strip()] = val.strip()
                elif "=" in attr_str:
                    key, val = attr_str.split("=")
                    kw_attrs[key.strip()] = val.strip()
            try:
                result.append(class_init(*pos_attrs, **kw_attrs))
            except TooDistantDateError as err:
                print(err)
    return result


def get_hours_before_deadline(arg_date, arg_deadline, arg_calendar):
    days_before_deadline = list(filter(lambda d: arg_date < d.date < arg_deadline, arg_calendar))
    return sum(map(lambda d: d.work_hours, days_before_deadline), timedelta(hours=0))


def get_hours_from_timedelta(td_obj: timedelta) -> int:
    return td_obj.seconds // 3600


def create_calendar(arg_tasks: [Task], arg_spec_days: [Day]) -> [Day]:
    result = []
    cur_date = date.today()
    # while cur_date < max(filter(lambda d: not d.is_weekend(), spec_days),
    #                      key=lambda d: d.date).date:
    max_deadline_date = max(arg_tasks, key=lambda t: t.deadline).deadline
    max_spec_days_date = max(filter(lambda d: not d.is_weekend(), arg_spec_days),
                             key=lambda d: d.date).date
    while cur_date < max(max_deadline_date, max_spec_days_date):
        work_hours = 4
        spec_dates = dict(zip(map(lambda d: d.date, arg_spec_days),
                              map(lambda d: d.work_hours, arg_spec_days)))
        if cur_date in spec_dates.keys():
            work_hours = get_hours_from_timedelta(spec_dates[cur_date])
        result.append(Day(cur_date, work_hours=work_hours))
        cur_date += timedelta(days=1)
    return result


if __name__ == "__main__":
    # types: better_first, better_last, mixed
    allocation_type = "better_first"
    weekends = []

    # get class lists
    task_pos_attr_names = ["name"]
    tasks = read_class_objs('tasks.txt', Task, task_pos_attr_names)
    day_pos_attr_names = ["date"]
    spec_days = read_class_objs('days.txt', Day, day_pos_attr_names)

    # print class lists
    print("Tasks:")
    task_attrs = ["name", "interest", "deadline"]
    print_class_objs(sorted(tasks, key=lambda tsk: tsk.interest, reverse=True),
                     *task_attrs)

    print("\nSpecial days:")
    day_attrs = ["date", "work_hours"]
    print_class_objs(sorted(spec_days, key=lambda d: d.date), *day_attrs)
    print()

    print("Calendar max_day:")
    calendar = create_calendar(tasks, spec_days)
    print(max(calendar, key=lambda d: d.date))
    print()

    print("Hours before deadline:")
    task_name = "Java spring tutor project"
    ex_deadline_date = next(filter(lambda t: t.name.lower() == task_name.lower(), tasks)).deadline
    # print(ex_deadline_date)
    ex_date_date = date.today()
    print(get_hours_before_deadline(ex_date_date, ex_deadline_date, calendar))

    # better first
    # if allocation_type == "better_first":
    #     tasks.sort(key=lambda tsk: (tsk.must_do, tsk.interest))
