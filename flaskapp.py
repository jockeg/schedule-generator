from flask import Flask, render_template, request, make_response
from datetime import date
from babel.dates import format_date
from schedule_generator import shift_day, year_dates, week_len, SweHolidays, helgdagar
from pay_calculator import pay, schedule, schedule_month
import pdfkit
import pandas as pd

holidays_se = SweHolidays(include_sundays=False)

vacationgrp1 = [25, 26, 27, 28]
freegrp1 = [29]
vacationgrp2 = [30, 31, 32, 33]
freegrp2 = [34]

# Months
months = {1: 'Januari',
          2: 'Februari',
          3: 'Mars',
          4: 'April',
          5: 'Maj',
          6: 'Juni',
          7: 'Juli',
          8: 'Augusti',
          9: 'September',
          10: 'Oktober',
          11: 'November',
          12: 'December'}


app = Flask(__name__)


@app.route('/')
def entry_page():
    return render_template('entry.html',
                           the_title='Hem',
                           year=date.today().year,)


@app.route('/schema', methods=['POST'])
def generate():
    year = request.form['year']
    dates = year_dates(int(year))
    return render_template('schema.html',
                           the_title='Schema ' + year,
                           year=year,
                           datum=dates,
                           shift_day=shift_day,
                           strftime=date.strftime,
                           format_date=format_date,
                           len=len,
                           int=int,
                           week_len=week_len,
                           holidays_se=holidays_se,
                           helgdagar=helgdagar,
                           vacationgrp1=vacationgrp1,
                           freegrp1=freegrp1,
                           vacationgrp2=vacationgrp2,
                           freegrp2=freegrp2,)


@app.route('/pdf', methods=['POST'])
def generatepdf():
    year = request.form['year']
    dates = year_dates(int(year))
    rendered = render_template('schema.html',
                               the_title='Schema ' + year,
                               year=year,
                               datum=dates,
                               shift_day=shift_day,
                               strftime=date.strftime,
                               format_date=format_date,
                               len=len,
                               int=int,
                               week_len=week_len,
                               holidays_se=holidays_se,
                               helgdagar=helgdagar,
                               vacationgrp1=vacationgrp1,
                               freegrp1=freegrp1,
                               vacationgrp2=vacationgrp2,
                               freegrp2=freegrp2,)

    options = {
        'enable-local-file-access': None,
        'orientation': 'Landscape',
        'margin-bottom': '5mm',
        'margin-top': '5mm',
        'margin-left': '5mm',
        'margin-right': '5mm',
        }
    css = 'static/pdf.css'
    config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')

    pdf = pdfkit.from_string(rendered, False, options=options, css=css,
                             configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Schema-{year}.pdf'

    return response


@app.route('/loneutrakning', methods=['POST'])
def calculate_pay():
    year = request.form['year']
    salary = float(request.form['salary'].replace(',', '.'))
    shift = request.form['shift']
    dates = schedule(int(year), int(shift))
    total_pay = 12 * salary
    month_pay = salary
    month = int(request.form['month'])
    dates_month = schedule_month(int(year), int(month), int(shift))
    skattetabell = int(request.form['skattetabell'])
    
    xl_file = 'https://www.skatteverket.se/download/18.339cd9fe17d1714c0771bae/1638974402658/M%C3%A5nadsl%C3%B6n%202022.xlsx'

    for date, workshift in dates.items():
        total_pay += pay(salary, date, workshift)
    
    for date, workshift in dates_month.items():
        month_pay += pay(salary, date, workshift)

    df = pd.read_excel(xl_file)
    df2 = df.loc[:, ['Tabellnr', 'Inkomst t.o.m.', 'Kolumn 1']]
    df3 = df2.set_index('Tabellnr')
    df4 = df3.loc[skattetabell]
    df5 = df4.set_index('Kolumn 1')
    result = df5['Inkomst t.o.m.'].sub(month_pay).abs().idxmin()
    
    return render_template('calc.html',
                           the_title='Lön ' + months.get(month) + ' ' + year,
                           salary=salary,
                           year=year,
                           shift=shift,
                           dates=dates,
                           pay=pay,
                           total_pay=total_pay,
                           month_pay=month_pay,
                           month=month,
                           months=months,
                           round=round,
                           result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
