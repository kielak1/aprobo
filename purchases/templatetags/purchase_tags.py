from django import template

register = template.Library()

@register.inclusion_tag('purchase_field_base.html')
def purchase_field_base(instance, field, field_label, freeze_all, alert, left):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'freeze_all': freeze_all,
        'alert': alert,
        'left' : left
    }
    return context

@register.inclusion_tag('purchase_field_multiple.html')
def purchase_field_multiple(instance, field, field_label, freeze_all):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'freeze_all': freeze_all,
    }
    return context

@register.inclusion_tag('purchase_field_no_form.html')
def purchase_field_no_form(instance, field_label):
    context = {
        'field_label': field_label,
        'instance': instance,
    }
    return context

@register.inclusion_tag('purchase_field_info.html')
def purchase_field_info(instance, field, field_label, freeze, alert):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'freeze_all': freeze,
        'alert': alert,
    }
    return context

@register.inclusion_tag('purchase_field_komentarz.html')
def purchase_field_komentarz(instance, field, field_label, status, rola):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'status': status,
        'rola' : rola,
     
    }
    return context


# @register.inclusion_tag('purchase_field_form_only.html')
# def purchase_field_form_only( field, field_label, freeze ):
#     context = {
#         'field_label': field_label,
#         'field': field,
#         'freeze_all': freeze,
#     }
#     return context