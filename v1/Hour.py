from datetime import timedelta, datetime


class InvalidHourError(Exception):
    """Error class for invalid Day"""
    pass


class WorkHours:
    def __init__(self, task, **kwargs):
        self.__task = task

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
    def date(self, date):
        self.__date = date

    @property
    def work_hours(self):
        return self.__work_hours

    @work_hours.setter
    def work_hours(self, work_hours):
        self.__work_hours = work_hours
