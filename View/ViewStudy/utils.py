from .models import *

menu = [{'title': 'Список', 'url_name': 'lVpattern'},
        {'title': 'Создать', 'url_name': 'CVpattern'},
        {'title': 'Изменить', 'url_name': 'UVpattern'},
        {'title': 'Удалить', 'url_name': 'Delpattern'},
        ]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        authors = Author.objects.all()
        context['menu'] = menu
        context['as'] = authors
        return context
