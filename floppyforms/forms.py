from django import forms
from django.template.loader import get_template
from django.utils.encoding import python_2_unicode_compatible

from .compat import get_context


__all__ = ('BaseForm', 'Form',)


@python_2_unicode_compatible
class LayoutRenderer(object):
    _render_as_template_name = 'floppyforms/_render_as.html'

    def _render_as(self, layout):
        template_node = get_template(self._render_as_template_name)
        context = get_context({
            'form': self,
            'layout': layout,
        })
        return template_node.render(context)

    def __str__(self):
        return self._render_as('floppyforms/layouts/default.html')

    def as_p(self):
        return self._render_as('floppyforms/layouts/p.html')

    def as_ul(self):
        return self._render_as('floppyforms/layouts/ul.html')

    def as_table(self):
        return self._render_as('floppyforms/layouts/table.html')


class BaseForm(LayoutRenderer, forms.BaseForm):
    pass


class Form(LayoutRenderer, forms.Form):
    pass
