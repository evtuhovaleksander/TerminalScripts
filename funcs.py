import datetime
def get_date(efir_date):
    if efir_date is None:
        efir_date = None
    else:
        if efir_date == '':
            efir_date = None
        else:
            efir_date = datetime.datetime.strptime(efir_date, "%d.%m.%Y %H:%M")
    return efir_date