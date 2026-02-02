from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary by key"""
    if dictionary is None:
        return None
    return dictionary.get(key)

@register.filter
def parse_date(date_str):
    """Parse a date string and return a datetime object"""
    if isinstance(date_str, str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return None
    return date_str

@register.filter
def format_date(date_obj, format_str):
    """Format a date object with the given format"""
    if date_obj:
        try:
            return date_obj.strftime(format_str)
        except:
            return str(date_obj)
    return ''
