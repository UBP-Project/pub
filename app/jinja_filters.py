from jinja2 import environment
def datetime_filter(dt):
    format = '%B %d, %Y'
    return dt.strftime(format)

def datetime_with_day_filter(dt):
    format = '%a, %B %d, %Y'
    return dt.strftime(format)

environment.DEFAULT_FILTERS['datetime'] = datetime_filter
environment.DEFAULT_FILTERS['datetime_with_day'] = datetime_with_day_filter