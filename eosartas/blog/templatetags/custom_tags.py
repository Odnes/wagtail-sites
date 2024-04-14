from django import template
from blog.models import Menu

register = template.Library()

@register.inclusion_tag('eosartas/templates/navbar.html', takes_context=True)
def navbar(context):
    return {
# TODO should select specifically for the navbar menu if the intention is to reuse
# the model for more menus
        'navbar': Menu.objects.all(),
        'request': context['request'],
    }
