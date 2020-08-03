from flask import Flask, render_template, request, make_response
from datetime import date
from schedule_generator import shift_day, year_dates, week_len, SweHolidays, helgdagar
from pay_calculator import pay, schedule
import pdfkit
import locale

holidays_se = SweHolidays(include_sundays=False)

vacationgrp1 = [25, 26, 27, 28]
freegrp1 = [29]
vacationgrp2 = [30, 31, 32, 33]
freegrp2 = [34]


app = Flask(__name__)


@app.route('/')
def entry_page():
    return render_template('entry.html',
                           the_title='Webapp')


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
        'margin-bottom': '0mm',
        'margin-top': '5mm',
        'margin-left': '0mm',
        'margin-right': '0mm',
        }
    css = 'static/pdf.css'
    config = pdfkit.configuration(wkhtmltopdf='./bin/wkhtmltopdf')

    pdf = pdfkit.from_string(rendered, False, options=options, css=css, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=Schema-{year}.pdf'

    return response


@app.route('/loneutrakning', methods=['POST'])
def calculate_pay():
    year = request.form['year']
    salary = int(request.form['salary'])
    shift = request.form['shift']
    dates = schedule(int(year), int(shift))
    total_pay = 12 * salary
    for date, workshift in dates.items():
        total_pay += pay(salary, date, workshift)
    return render_template('calc.html',
                           the_title='Lön ' + year,
                           salary=salary,
                           year=year,
                           shift=shift,
                           dates=dates,
                           pay=pay,
                           total_pay=total_pay,)


if __name__ == '__main__':
    # Set locale for correct display of weekdays
    locale.setlocale(locale.LC_ALL, 'sv_SE')

    app.run(debug=False, host='0.0.0.0')
