from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def convert_time(time):
    am_pm = "am"
    time_split = time.split('.')
    if len(time_split) >= 2:
        hours, minutes = time_split[0], time_split[1]
        if hours.isnumeric() and minutes.isnumeric():
            hours = int(hours)
            if hours >= 12:
                if hours > 12:
                    hours -= 12
                am_pm = "pm"

            return str(hours) + ":" + minutes + am_pm
    else:
        return ""
