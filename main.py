from datetime import timedelta, datetime


class InvalidTaskError(Exception):
    # error class for raise errors)))
    pass


class Task:
    # work_hours in day
    __day_work_hours = timedelta(hours=4)

    def __init__(self, name: str, **kwargs):
        # if (kwargs.get("deadline", None) is None
        #         and kwargs.get("must_do", None) is None):
        #     raise InvalidTaskError(
        #         "You can't have deadline and must_do empty at the same time")

        # Task name
        self.__name = name

        # Task deadline(default=actual date + 90 days)
        if "deadline" in kwargs:
            self.__deadline = datetime.strptime(kwargs["deadline"], "%d.%m.%Y")
        else:
            self.__deadline = datetime.now() + timedelta(days=90)

        # interest from 1 to 10(default=5)
        self.__interest = int(kwargs.get("interest", 5))

        # lead time in hours(default=4 hours)
        if "work_hours" in kwargs:
            self.__work_hours = timedelta(hours=int(kwargs["work_hours"]))
        else:
            self.__work_hours = self.__day_work_hours

        # Task must do(default=True)
        self.__must_do = False if kwargs.get("must_do", None) == "False" else True

    def __str__(self):
        return (f"Task name: {self.__name}, deadline: {self.__deadline}, "
                f"interest: {self.__interest}/10, work_hours: {self.__work_hours}, "
                f"must_do: {self.__must_do} ")

    def __repr__(self):
        return (f"Task(name={self.__name}, deadline={self.__deadline}, "
                f"interest={self.__interest}, work_hours={self.__work_hours}, "
                f"must_do={self.__must_do})")

    @property
    def interest(self):
        return self.__interest

    @interest.setter
    def interest(self, interest):
        self.interest = interest

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, deadline):
        self.__deadline = deadline

    @property
    def must_do(self):
        return self.__must_do

    @must_do.setter
    def must_do(self, must_do):
        self.__must_do = must_do


class Day:
    def __init__(self, date, **kwargs):
        self.__date = date
        # self.__weekend = True if kwargs.get("weekend", None) == "True" else: False
        self.__work_hours = timedelta(hours=int(kwargs.get("work_hours", 4)))

    def __repr__(self):
        return f"Day(date={self.__date}, day_work_hours={self.__work_hours})"

    def __str__(self):
        return f"Day date: {self.__date}, day_work_hours={self.__work_hours}"

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date):
        self.__date = date

    @property
    def work_hours(self):
        return self.__work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self.__work_hours = work_hours


def print_class_objs(input_list: [], *attrs):
    for elem in input_list:
        for attr in attrs:
            result = getattr(elem, attr, "No attr")
            if isinstance(result, datetime):
                result = result.date()
            print(f"{attr}={result}", end=", ")
        print()


def read_class_objs(file_name: str, class_init, * pos_attr_names) -> []:
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
            result.append(class_init(*pos_attrs, **kw_attrs))
    return result


if __name__ == "__main__":
    # types: better_first, better_last, mixed
    allocation_type = "better_first"
    weekends = []

    # get class lists
    task_pos_attr_names = ["name"]
    tasks = read_class_objs('tasks.txt', Task, task_pos_attr_names)
    day_pos_attr_names = ["date"]
    days = read_class_objs('days.txt', Day, day_pos_attr_names)

    # print class lists
    task_attrs = ["name", "interest", "deadline"]
    print_class_objs(sorted(tasks, key=lambda tsk: tsk.interest, reverse=True),
                     *task_attrs)
    day_attrs = ["date", "work_hours"]
    print_class_objs(sorted(days, key=lambda d: d.date), *day_attrs)

    # better first
    if allocation_type == "better_first":
        tasks.sort(key=lambda tsk: (tsk.must_do, tsk.interest))
