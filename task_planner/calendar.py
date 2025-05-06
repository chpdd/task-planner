import datetime as dt

from task_planner.day import Day, Task


class Calendar:
    def __init__(self, manual_days: [Day] = None, start_date: dt.date = dt.date.today(),
                 dflt_day_work_hours: int = 4, dflt_task_work_hours: int = 2, max_date: dt.date = None) -> None:
        self._manual_days: [Day] = [] if manual_days is None else manual_days
        self._manual_date_work_hours: {dt.date: int} = {day.date: day.work_hours for day in self.manual_days}
        self._dflt_day_work_hours: int = dflt_day_work_hours
        self._dflt_task_work_hours: int = dflt_task_work_hours
        self._start_date: dt.date = start_date
        self._days: [Day] = []
        self._near_fillable_day_index: int = -1

        self.init_days(max_date)

    def __getitem__(self, index: int) -> Day:
        return self._days[index]

    def __len__(self) -> int:
        return len(self._days)

    @property
    def start_date(self) -> dt.date:
        return self._start_date

    @property
    def near_fillable_day(self) -> Day:
        return self._days[self._near_fillable_day_index]

    @property
    def dflt_day_work_hours(self) -> int:
        return self._dflt_day_work_hours

    @dflt_day_work_hours.setter
    def dflt_day_work_hours(self, work_hours: int) -> None:
        self._dflt_day_work_hours = work_hours

    @property
    def dflt_task_work_hours(self) -> int:
        return self._dflt_task_work_hours

    @dflt_task_work_hours.setter
    def dflt_task_work_hours(self, work_hours: int) -> None:
        self._dflt_task_work_hours = work_hours

    @property
    def manual_days(self) -> [Day]:
        return self._manual_days

    @manual_days.setter
    def manual_days(self, manual_days: [Day]) -> None:
        self._manual_days = manual_days
        self._manual_date_work_hours: {dt.date: int} = {day.date: day.work_hours for day in manual_days}
        self.init_days()

    @property
    def manual_date_work_hours(self) -> {dt.date: int}:
        return self._manual_date_work_hours

    @property
    def days(self) -> [Day]:
        return self._days

    @property
    def last_added_day_date(self) -> dt.date:
        if len(self.days):
            return self.days[-1].date
        return self.start_date - dt.timedelta(days=1)

    def init_days(self, max_date: dt.date = None) -> None:
        max_date = self.start_date if max_date is None else max_date
        self._days: [Day] = []
        while self.last_added_day_date <= max_date:
            self.add_day()
        self._near_fillable_day_index: int = -1
        self.next_fillable_day()

    def clean_calendar(self):
        for day in self.days:
            day.clean_schedule()
        self._near_fillable_day_index = -1
        self.next_fillable_day()

    def add_day(self) -> None:
        date = self.last_added_day_date + dt.timedelta(days=1)
        work_hours = self.manual_date_work_hours.get(date, self.dflt_day_work_hours)
        self.days.append(Day(date=date, work_hours=work_hours))

    def next_fillable_day(self) -> None:
        self._near_fillable_day_index += 1
        while self._near_fillable_day_index >= len(self.days) or self.near_fillable_day.is_task_filled():
            if self._near_fillable_day_index >= len(self.days):
                self.add_day()
            elif self.near_fillable_day.is_task_filled():
                self._near_fillable_day_index += 1

    def next_fillable_day_v2(self) -> None:
        """
        Same as next_fillable_day, but no double-checking of conditions and more cumbersome.
        """
        max_day_flag, free_hours_flag = True, True
        while max_day_flag or free_hours_flag:
            if self._near_fillable_day_index >= len(self.days):
                self.add_day()
                max_day_flag = False
                continue
            else:
                max_day_flag = True

            self._near_fillable_day_index += 1
            if self.near_fillable_day.free_hours == 0:
                free_hours_flag = False
            else:
                free_hours_flag = True

    def add_task(self, task: Task, work_hours: int) -> None:
        day = self.near_fillable_day
        while work_hours:
            while day.is_task_filled():
                self.next_fillable_day()
                day = self.near_fillable_day
            work_hours = day.add_task(task, work_hours)

    def add_task_before_date(self, task: Task, work_hours: int, date: dt.date) -> None:
        day_i = len(self.days) - 1
        while self.days[day_i].date >= date:
            day_i -= 1
        while work_hours:
            while self.days[day_i].is_task_filled():
                day_i -= 1
            work_hours = self.days[day_i].add_task(task, work_hours)

    def get_free_hours_before_date(self, left_date: dt.date, right_date: dt.date) -> int:
        result = 0
        while right_date >= self.last_added_day_date:
            self.add_day()
        for day in self.days:
            if day.date >= right_date:
                break
            if day.date >= left_date:
                result += day.free_hours
        return result
