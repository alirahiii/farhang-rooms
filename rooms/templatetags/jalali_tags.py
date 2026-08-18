import jdatetime
from django import template
from django.utils import timezone

register = template.Library()

PERSIAN_DIGITS = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')


@register.filter
def jalali(value):
    if not value:
        return ''
    local_value = timezone.localtime(value)
    jalali_date = jdatetime.datetime.fromgregorian(datetime=local_value)
    formatted = jalali_date.strftime('%Y/%m/%d')
    return formatted.translate(PERSIAN_DIGITS)


@register.filter
def persian_digits(value):
    if value is None:
        return ''
    return str(value).translate(PERSIAN_DIGITS)
