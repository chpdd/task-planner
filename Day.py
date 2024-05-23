from datetime import timedelta, date, datetime


class InvalidDayError(Exception):
    """Error class for invalid Day"""
    pass


class TooDistantDateError(Exception):
    """Error class for raise if task too far away"""
    pass


class Day:
    def __init__(self, date_, **kwargs):
        if isinstance(date_, str):
            self.__date = datetime.strptime(date_, "%d.%m.%Y").date()
        elif isinstance(date_, date):
            self.__date = date_
        self.__work_hours = timedelta(hours=int(kwargs.get("work_hours", 4)))

    def __repr__(self):
        return f"Day(date={self.__date}, day_work_hours={self.__work_hours})"

    def __str__(self):
        return f"Day date: {self.__date}, day_work_hours={self.__work_hours}"

    def is_weekend(self):
        if self.__work_hours == timedelta(hours=0):
            return True
        return False

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, date_):
        self.__date = date_

    @property
    def work_hours(self):
        return self.__work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self.__work_hours = work_hours
