from django import forms, template
from django.utils.encoding import python_2_unicode_compatible

from .templatetags.floppyforms import FormNode


__all__ = ('BaseForm', 'Form',)


@python_2_unicode_compatible
class LayoutRenderer(object):
    _template_node = FormNode(
        'form',
        [template.Variable('form')],
        {
            'using': template.Variable('layout'),
            'only': False,
            'with': None,
        })

    def _render_as(self, layout):
        context = template.Context({
            'form': self,
            'layout': layout,
        })
        return self._template_node.render(context)

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
