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
        if "task_work_hours" in kwargs:
            self.__task_work_hours = timedelta(hours=int(kwargs["task_work_hours"]))
        else:
            self.__task_work_hours = self.__day_work_hours

        # Task must do(default=True)
        self.__must_do = False if kwargs.get("must_do", True) == "False" else True

    def __str__(self):
        return (f"Task name: {self.__name}, deadline: {self.__deadline}, "
                f"interest: {self.__interest}/10, task_work_hours: {self.__task_work_hours}, "
                f"must_do: {self.__must_do} ")

    def __repr__(self):
        return (f"Task(name={self.__name}, deadline={self.__deadline}, "
                f"interest={self.__interest}, task_work_hours={self.__task_work_hours}, "
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


def print_tasks_list(tasks_list: list[Task], *attrs):
    for tsk in tasks_list:
        for attr in attrs:
            if attr == "deadline":
                print(f"{attr}: {getattr(tsk, attr, "No attr").date()}", end=", ")
            else:
                print(f"{attr}: {getattr(tsk, attr, "No attr")}", end=", ")
            # print(tsk.func())
        print()


def sort_by_interest(tasks_list: [Task]):
    return sorted(tasks_list, key=lambda tsk: tsk.interest, reverse=True)


if __name__ == "__main__":
    # types: better_first, better_last, mixed
    allocation_type = "better_first"
    weekends = []
    tasks = []
    with open('input.txt', 'r') as f_input:
        lines = f_input.readlines()
        for line in lines:
            strings = line.strip().split(",")
            kwargs = dict()
            name = strings[0].strip()
            for string in strings[1:]:
                if ":" in string:
                    key, arg = string.strip().split(":")
                    kwargs[key.strip()] = arg.strip()
                elif "=" in string:
                    key, arg = string.strip().split("=")
                    kwargs[key.strip()] = arg.strip()
            tasks.append(Task(name, **kwargs))
            # print(name, kwargs)

    attrs = ["name", "interest", "deadline"]
    print_tasks_list(sort_by_interest(tasks), *attrs)

    # better first
    if allocation_type == "better_first":
        pass
