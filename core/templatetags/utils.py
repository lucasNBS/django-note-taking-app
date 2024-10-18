from django import template

register = template.Library()

@register.filter()
def filter_current_user_like(value, user):
  return value.filter(user=user).exists()

@register.filter()
def rest(value1, value2):
  return value1 % value2