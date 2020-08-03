import calendar
import datetime as dt
import holidays
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta


shifts = ('Fi', 'F', 'E', 'E', 'N', 'Na', 'E',
          'L', 'L', 'L', 'L', 'F', 'D', 'F',
          'E', 'E', 'N', 'N', 'L', 'L', 'L',
          'L', 'L', 'F', 'F', 'E', 'L', 'N',
          'N', 'N', 'L', 'L', 'L', 'L', 'L')


helgdagar = {'Nyårsdagen': 'ND', 'Trettondedag jul': 'TD', 'Långfredagen': 'LF',
             'Påskafton': 'PA', 'Påskdagen': 'PD', 'Annandag påsk': 'AP',
             'Första maj': '1M', 'Kristi himmelsfärdsdag': 'KH',
             'Sveriges nationaldag': 'ND', 'Pingstafton': 'PA', 'Pingstdagen':
             'PD', 'Midsommarafton': 'MA', 'Midsommardagen': 'MD',
             'Alla helgons dag': 'AH', 'Julafton': 'JA', 'Juldagen': 'JD',
             'Annandag jul': 'AD', 'Nyårsafton': 'NA'}


class SweHolidays(holidays.SE):
    def _populate(self, year):
        holidays.SE._populate(self, year)

        e = easter(year)
        easter_saturday = e - relativedelta(days=1)
        pentecost_evening = e + relativedelta(days=48)

        self[easter_saturday] = "Påskafton"
        self[pentecost_evening] = "Pingstafton"


cal = calendar.Calendar(firstweekday=0)


def week_len(week, month, row):
    """Returns the length of week in month,
    not counting days which are outside month"""

    days_week = 0
    for day in week:
        if day.month == row.index(month) + 1 or day.month == row.index(month) + 7:
            days_week += 1
    return days_week


def year_dates(year):
    """Returns a list of dates of year, with 6 months row length"""

    return cal.yeardatescalendar(year, 6)


def shift_day(date, shift):
    """Returns the string corresponding to date from tuple shifts"""

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
