from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        return "R$ {:,.2f}".format(float(value)).replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"
