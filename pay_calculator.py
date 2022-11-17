import datetime as dt
import holidays
from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR, SA

from holidays.constants import JAN, MAR, MAY, JUN, OCT, DEC
from holidays.constants import MON, THU, FRI, SAT, SUN
from holidays.holiday_base import HolidayBase
# from schedule_generator import SweHolidays

# A tuple of the shift pattern: strings to be associated with dates
shifts = ('Fi', 'F', 'E', 'E', 'N', 'Na', 'E',
          'L', 'L', 'L', 'L', 'F', 'D', 'F',
          'E', 'E', 'N', 'N', 'L', 'L', 'L',
          'L', 'L', 'F', 'F', 'E', 'L', 'N',
          'N', 'N', 'L', 'L', 'L', 'L', 'L')


# holidays_se = SweHolidays(include_sundays=False)


class BigHolidays(HolidayBase):
    def __init__(self, **kwargs):
        self.country = "SE"
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):

        # ========= Static holidays =========
        self[date(year, JAN, 1)] = "Nyårsdagen"

        # self[date(year, JAN, 6)] = "Trettondedag jul"

        # Source: https://sv.wikipedia.org/wiki/F%C3%B6rsta_maj
        if year >= 1939:
            self[date(year, MAY, 1)] = "Första maj"

        # Source: https://sv.wikipedia.org/wiki/Sveriges_nationaldag
        if year >= 2005:
            self[date(year, JUN, 6)] = "Sveriges nationaldag"

        self[date(year, DEC, 24)] = "Julafton"
        self[date(year, DEC, 25)] = "Juldagen"
        self[date(year, DEC, 26)] = "Annandag jul"
        self[date(year, DEC, 31)] = "Nyårsafton"

        # ========= Moving holidays =========
        e = easter(year)
        maundy_thursday = e - rd(days=3)
        good_friday = e - rd(days=2)
        easter_saturday = e - rd(days=1)
        resurrection_sunday = e
        easter_monday = e + rd(days=1)
        # ascension_thursday = e + rd(days=39)
        pentecost = e + rd(days=49)
        pentecost_day_two = e + rd(days=50)

        assert maundy_thursday.weekday() == THU
        assert good_friday.weekday() == FRI
        assert easter_saturday.weekday() == SAT
        assert resurrection_sunday.weekday() == SUN
        assert easter_monday.weekday() == MON
        # assert ascension_thursday.weekday() == THU
        assert pentecost.weekday() == SUN
        assert pentecost_day_two.weekday() == MON

        self[good_friday] = "Långfredagen"
        self[resurrection_sunday] = "Påskdagen"
        self[easter_monday] = "Annandag påsk"
        # self[ascension_thursday] = "Kristi himmelsfärdsdag"
        self[pentecost] = "Pingstdagen"
        if year <= 2004:
            self[pentecost_day_two] = "Annandag pingst"

        # Midsummer evening. Friday between June 19th and June 25th
        self[date(year, JUN, 19) + rd(weekday=FR)] = "Midsommarafton"

        # Midsummer day. Saturday between June 20th and June 26th
        if year >= 1953:
            self[date(year, JUN, 20) + rd(weekday=SA)] = "Midsommardagen"
        else:
            self[date(year, JUN, 24)] = "Midsommardagen"
            # All saints day. Friday between October 31th and November 6th
        # self[date(year, OCT, 31) + rd(weekday=SA)] = "Alla helgons dag"

        if year <= 1953:
            self[date(year, MAR, 25)] = "Jungfru Marie bebådelsedag"

        # e = easter(year)
        easter_saturday = e - rd(days=1)
        pentecost_evening = e + rd(days=48)

        self[easter_saturday] = "Påskafton"
        self[pentecost_evening] = "Pingstafton"


class SmallHolidays(HolidayBase):
    def __init__(self, **kwargs):
        self.country = "SE"
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):

        # ========= Static holidays =========
        self[date(year, JAN, 6)] = "Trettondedag jul"

        # ========= Moving holidays =========
        e = easter(year)
        ascension_thursday = e + rd(days=39)

        assert ascension_thursday.weekday() == THU

        self[ascension_thursday] = "Kristi himmelsfärdsdag"

        self[date(year, OCT, 31) + rd(weekday=SA)] = "Alla helgons dag"


holidays_se = BigHolidays()
small_holidays_se = SmallHolidays()


def pay(base_pay, date, shift_day, vacation_weeks):
    ob1 = 27.44 # 16:30-22:30
    ob2 = 34.91 # 22:30-06:30
    ob3 = 76.80 # Weekends/small holidays
    ob4 = 170.82 # Big holidays

    if shift_day == 'L':
        return 0
    elif date.isocalendar().week in vacation_weeks:
        return 0
    elif shift_day == 'Fi':
        if date in holidays_se:
            return 0.75 * ob2 + 9.75 * ob4
        elif date in small_holidays_se:
            return 0.75 * ob2 + 9.75 * ob3
        else:
            return 0.75 * ob2
    elif shift_day == 'F':
        if date in holidays_se:
            return 0.75 * ob2 + 8.25 * ob4
        elif date in small_holidays_se:
            return 0.75 * ob2 + 8.25 * ob3
        elif date.weekday() in range(5, 7):
            return 0.75 * ob2 + 8.25 * ob3
        else:
            return 0.75 * ob2
    elif shift_day == 'D':
        if date in holidays_se:
            return 0.75 * ob2 + 1.5 * ob1 + 12.25 * ob4
        elif date in small_holidays_se:
            return 0.75 * ob2 + 1.5 * ob1 + 12.25 * ob3
        else:
            return 0.75 * ob2 + 1.5 * ob1 + 12.25 * ob3
    elif shift_day == 'E':
        if date in holidays_se:
            return 5.5 * ob1 + 8.25 * ob4
        elif date in small_holidays_se:
            return 5.5 * ob1 + 8.25 * ob3
        elif date.weekday() == 6:
            return 5.5 * ob1 + 8.25 * ob3
        else:
            return 5.5 * ob1
    elif shift_day == 'N':
        if date + dt.timedelta(days=1) in holidays_se:
            return 0.75 * ob1 + 7.5 * ob2 + 8.25 * ob4
        elif date == dt.date(date.year, 1, 1):
            return 0.75 * ob1 + 7.5 * ob2 + 8.25 * ob4
        elif date + dt.timedelta(days=1) in small_holidays_se:
            return 0.75 * ob1 + 7.5 * ob2 + 7.5 * ob3
        elif date in small_holidays_se:
            return 0.75 * ob1 + 7.5 * ob2 + 0.75 * ob3
        elif date.weekday() == 4:
            return 0.75 * ob1 + 7.5 * ob2 + 7.5 * ob3
        elif date.weekday() == 6:
            return 0.75 * ob1 + 7.5 * ob2 + 0.75 * ob3
        else:
            return 0.75 * ob1 + 7.5 * ob2
    elif shift_day == 'Na':
        if date + dt.timedelta(days=1) in holidays_se:
            return 4.75 * ob1 + 7.5 * ob2 + 12.25 * ob4
        else:
            return 4.75 * ob1 + 7.5 * ob2 + 12.25 * ob3


def shift_day(date, shift):
    """Return the string corresponding to date from tuple shifts"""

    offset = 0
    if shift == 1:
        offset += 21
    if shift == 2:
        offset += 0
    if shift == 3:
        offset += 7
    if shift == 4:
        offset += 28
    if shift == 5:
        offset += 14

    # Define the date from where to start counting
    first_shift_day = dt.date(2018, 12, 31)
    return shifts[(int((date - first_shift_day).days) + offset) % len(shifts)]


def year_dates(year):
    """Return a list of datetime objects for the year"""
    start_date = dt.date(year, 1, 1)
    end_date = dt.date(year + 1, 1, 1)
    return [start_date + dt.timedelta(i)
            for i in range(int((end_date - start_date).days))]


def month_dates(year, month):
    """Return a list of datetime objects for the month -1 in year"""
    if month == 1:
        start_date = dt.date(year - 1, 12, 1)
    else:
        start_date = dt.date(year, month - 1, 1)
    end_date = dt.date(year, month, 1)
    return [start_date + dt.timedelta(i)
            for i in range(int((end_date - start_date).days))]


def schedule(year, shift):
    """Return a dict with date objects as keys and shift worked as values"""
    return {date: shift_day(date, shift) for date in year_dates(year)}


def schedule_month(year, month, shift):
    return {date: shift_day(date, shift) for date in month_dates(year, month)}


def work_schedule(year, shift):
    """Return a list of tuples with
        week number, day of month, weekday, and shift worked"""
    return [[single_date.strftime('%V'),
             single_date.strftime('%d'),
             single_date.strftime('%a'),
             shift_day(single_date, shift)]
            for single_date in year_dates(year)]


lista = year_dates(2019)

work_times = {'Fi': (dt.time(5, 45), dt.time(15, 30)),
              'F': (dt.time(5, 45), dt.time(14)),
              'E': (dt.time(13, 45), dt.time(22)),
              'N': (dt.time(21, 45), dt.time(6)),
              'Na': (dt.time(17, 45), dt.time(6)),
              'D': (dt.time(5, 45), dt.time(18))}


divisors = {600: (dt.time(17), dt.time(6)),
            270: dt.time(17)}
