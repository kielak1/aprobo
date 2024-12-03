from django import template
import re

register = template.Library()

@register.filter
def to_doc_domain(url):
    parts = url.split("//", 1)
    if len(parts) == 2:
        subdomain = 'doc.' + parts[1].split("/", 1)[0]
        return parts[0] + '//' + subdomain
    return url

@register.filter
def to_stat_domain(url):
    parts = url.split("//", 1)
    if len(parts) == 2:
        subdomain = 'stat.' + parts[1].split("/", 1)[0]
        return parts[0] + '//' + subdomain
    return url

