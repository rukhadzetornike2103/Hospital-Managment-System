from enum import Enum, auto
import datetime


class ShiftType(Enum):
    NIGHT = "Night"
    DAY = "Day"
    SPECIAL = "Special"


class Shift:
    def __init__(self, start_date_time, end_date_time, shift_type):

        self._start_date_time = start_date_time
        self._end_date_time = end_date_time
        if isinstance(shift_type, ShiftType):
            self._shift_type = shift_type
        else:
            raise TypeError("Must be a valid Shift type.")

    @property
    def start_date_time(self):
        return self._start_date_time

    @property
    def end_date_time(self):
        return self._end_date_time

    @property
    def shift_type(self):
        return self._shift_type


