import datetime as dt
from schedule_generator import SweHolidays

# A tuple of the shift pattern: strings to be associated with dates
shifts = ('Fi', 'F', 'E', 'E', 'N', 'Na', 'E',
          'L', 'L', 'L', 'L', 'F', 'D', 'F',
          'E', 'E', 'N', 'N', 'L', 'L', 'L',
          'L', 'L', 'F', 'F', 'E', 'L', 'N',
          'N', 'N', 'L', 'L', 'L', 'L', 'L')


holidays_se = SweHolidays(include_sundays=False)


def pay(base_pay, date, shift_day):
    if shift_day == 'L':
        return 0
    elif shift_day == 'Fi':
        if date not in holidays_se and date - dt.timedelta(days=1) not in holidays_se:
            return (base_pay / 270) * 0.25
        elif date not in holidays_se and date - dt.timedelta(days=1) in holidays_se:
            return ((base_pay / 270) + (base_pay / 110)) * 0.25
        elif date in holidays_se and date - dt.timedelta(days=1) not in holidays_se:
            return ((base_pay / 270) * 8.25) + ((base_pay / 110) * 8)
        else:
            return ((base_pay / 270) + (base_pay / 110)) * 8.25
    elif shift_day == 'F':
        if date not in holidays_se and date - dt.timedelta(days=1) not in holidays_se and date.weekday() not in range(5, 7):
            return (base_pay / 600) * 0.25
        elif date not in holidays_se and date - dt.timedelta(days=1) in holidays_se:
            return ((base_pay / 270) + (base_pay / 110)) * 0.25
        elif date in holidays_se and date - dt.timedelta(days=1) not in holidays_se and date.weekday() not in range(5, 7):
            return ((base_pay / 270) * 8) + ((base_pay / 110) * 8) + ((base_pay / 600) * 0.25)
        elif date in holidays_se and date - dt.timedelta(days=1) in holidays_se:
            return ((base_pay / 270) + (base_pay / 110)) * 8.25
        elif date.weekday() in range(5, 7):
            return (base_pay / 270) * 8.25
    elif shift_day == 'D':
        if date in holidays_se and date - dt.timedelta(days=1) in holidays_se:
            return ((base_pay / 270) * 12.25) + ((base_pay / 110) * 12.25)
        elif date in holidays_se and date - dt.timedelta(days=1) not in holidays_se:
            return ((base_pay / 270) * 12.25) + ((base_pay / 110) * 12)
        elif date not in holidays_se and date - dt.timedelta(days=1) in holidays_se:
            return ((base_pay / 270) * 12.25) + ((base_pay / 110) * 0.25)
        elif date not in holidays_se and date - dt.timedelta(days=1) not in holidays_se:
            return (base_pay / 270) * 12.25
    elif shift_day == 'E':
        if date not in holidays_se and date.weekday() not in range(4, 7):
            return (base_pay / 600) * 5
        elif date in holidays_se:
            return ((base_pay / 270) * 8.25) + ((base_pay / 110) * 8.25)
        elif date.weekday() in range(5, 7):
            return (base_pay / 270) * 8.25
        elif date.weekday() == 4:
            return (base_pay / 270) * 5
    elif shift_day == 'N':
        if date in holidays_se:
            return ((base_pay / 270) * 8.25) + ((base_pay / 110) * 8.25)
        elif date.weekday() in range(4, 7):
            return (base_pay / 270) * 8.25
        else:
            return (base_pay / 600) * 8.25
    elif shift_day == 'Na':
        if date in holidays_se:
            return ((base_pay / 270) * 12.25) + ((base_pay / 110) * 12.25)
        else:
            return 4.75 * 27.44 + 12.25 * 76.80 + 7.5 * 34.91


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
