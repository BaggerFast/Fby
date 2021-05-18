from django import template
register = template.Library()


@register.filter
def index(value, arg):
    try:
        return value[arg]
    except IndexError:
        return None
