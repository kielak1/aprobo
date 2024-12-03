from django import template

register = template.Library()

@register.filter(name='negate')
def negate(value):
    return not value

@register.inclusion_tag('need_domain_header.html')
def need_domain_header( status_akceptacji, domena ):
    context = {
        'status_akceptacji': status_akceptacji,
        'domena': domena,
    }
    return context

@register.inclusion_tag('need_field.html')
def need_field( level,instance, field, label, is_editor, is_freeze, typ, parent, clear, alert):
    context = {
        'level': level,
        'instance': instance,
        'field': field,        
        'label': label,
        'is_editor' : is_editor,
        'is_freeze': is_freeze,
        'typ' : typ,
        'parent' : parent,
        'clear' : clear,
        'alert' : alert,
    }
    return context

@register.inclusion_tag('need_field_base.html')
def need_field_base(instance, field, field_label, freeze_all, alert, left):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'freeze_all': freeze_all,
        'alert': alert,
        'left' : left
    }
    return context


@register.inclusion_tag('need_field_info.html')
def need_field_info(instance, field, field_label, freeze, alert):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'freeze_all': freeze,
        'alert': alert,
    }
    return context

@register.inclusion_tag('need_field_komentarz.html')
def need_field_komentarz(instance, field, field_label, status, rola):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'status': status,
        'rola' : rola,
     
    }
    return context

@register.inclusion_tag('need_field_komentarz_dziedzinowy.html')
def need_field_komentarz_dziedzinowy(instance, field, field_label, status, rola):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'status': status,
        'rola' : rola,
     
    }
    return context

@register.inclusion_tag('need_field_form_only.html')
def need_field_form_only( field, field_label, freeze ):
    context = {
        'field_label': field_label,
        'field': field,
        'freeze_all': freeze,
    }
    return context

@register.inclusion_tag('buton.html')
def buton( tryb, onclick, komunikat, etykieta ):
    context = {
        'tryb':tryb, 
        'onclick':onclick, 
        'komunikat':komunikat, 
        'etykieta':etykieta,
    }
    return context

@register.inclusion_tag('need_field_komentarz_architekta.html')
def need_field_komentarz_architekta(instance, field, field_label, status, rola):
    context = {
        'field_label': field_label,
        'instance': instance,
        'field': field,
        'status': status,
        'rola' : rola,
     
    }
    return context

