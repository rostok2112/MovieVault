from django.utils.safestring import mark_safe
from django import forms


class ImageWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = f'<img src="{value}" width="200" />' if value else ''
        return mark_safe(html)