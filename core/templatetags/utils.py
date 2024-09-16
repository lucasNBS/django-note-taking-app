from django import template

register = template.Library()

@register.filter()
def filter_current_user_like(value, user):
  return value.filter(user=user).exists()