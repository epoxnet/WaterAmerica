from datetime import datetime

def countdown_timer(move_date):
    def datetime_difference(date1, date2):
        return date1 - date2
    if move_date:
        return datetime_difference(move_date, datetime.utcnow())
    return datetime_difference(datetime.utcnow(), datetime.utcnow())