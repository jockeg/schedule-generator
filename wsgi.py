from flaskapp import app

application = app

if __name__ == '__main__':
    # Set locale for correct display of weekdays
    locale.setlocale(locale.LC_ALL, 'sv_SE')
    application.run()
