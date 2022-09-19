from django import template

from ..views import ARRAY_MANAGER


register = template.Library()


@register.inclusion_tag('app/arrays.html')
def show_arrays(mutable: bool = False):
    arrays = ARRAY_MANAGER.objects

    context: dict = {
        'arrays': arrays,
        'mutable': mutable
    }
    return context
