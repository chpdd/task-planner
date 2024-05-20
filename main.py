from datetime import timedelta, datetime


class InvalidTaskError(Exception):
    # error class for raise errors)))
    pass


class Task:
    # work_hours in day
    __work_hours = timedelta(hours=4)

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
        if "lead_time" in kwargs:
            self.__lead_time = timedelta(hours=int(kwargs["lead_time"]))
        else:
            self.__lead_time = self.__work_hours

        # Task must do(default=True)
        self.__must_do = False if kwargs.get("must_do", True) == "False" else True

    def __str__(self):
        return (f"Task name: {self.__name}, deadline: {self.__deadline}, "
                f"interest: {self.__interest}/10, lead_time: {self.__lead_time}, "
                f"must_do: {self.__must_do} ")

    def __repr__(self):
        return (f"Task(name={self.__name}, deadline={self.__deadline}, "
                f"interest={self.__interest}, lead_time={self.__lead_time}, "
                f"must_do={self.__must_do})")


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
    for task in tasks:
        print(task)
        # print(task._Task__name, task._Task__deadline, task._Task__interest,
        # task._Task__lead_time, task._Task__must_do)
