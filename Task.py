from datetime import timedelta, datetime, date


class InvalidTaskError(Exception):
    """Error class for invalid Task"""
    pass


class TooDistantDateError(Exception):
    """Error class for raise if task too far away"""
    pass


class Task:
    # work_hours in day
    __day_work_hours = timedelta(hours=4)

    def __init__(self, name: str, **kwargs):
        # if (kwargs.get("deadline", None) is None
        #         and kwargs.get("must_do", None) is None):
        #     raise InvalidTaskError(
        #         "You can't have deadline and must_do empty at the same time")
        if ("deadline" in kwargs and
                datetime.strptime(kwargs["deadline"],"%d.%m.%Y").date() > date.today() + timedelta(days=365)):
            raise TooDistantDateError("The planned date is too far away.")

        # Task name
        self.__name = name

        # Task deadline(default=actual date + 90 days)
        if "deadline" in kwargs:
            self.__deadline = datetime.strptime(kwargs["deadline"], "%d.%m.%Y").date()
        else:
            self.__deadline = date.today() + timedelta(days=90)

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
    def deadline(self, deadline: datetime.date):
        self.__deadline = deadline

    @property
    def must_do(self):
        return self.__must_do

    @must_do.setter
    def must_do(self, must_do):
        self.__must_do = must_do
