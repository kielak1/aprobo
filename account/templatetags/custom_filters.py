
from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group):
    return user.groups.filter(name=group.name).exists()




# from django.template.defaultfilters import stringfilter

# @register.filter
# @stringfilter
# def strip(value):
#     """Usuwa początkowe i końcowe białe znaki z ciągu znaków."""
#     return value.strip() if value else value
