from django import forms, template
from django.utils.encoding import python_2_unicode_compatible

from .templatetags.floppyforms import FormNode
from .widgets import Widget, MultiWidget, SelectDateWidget


__all__ = ('BaseForm', 'Form',)


class BoundField(forms.forms.BoundField):
    def as_widget(self, widget=None, attrs=None, only_initial=False, **kwargs):
        """
        Renders the field by rendering the passed widget, adding any HTML
        attributes passed as attrs.  If no widget is specified, then the
        field's default widget will be used.
        """
        if not widget:
            widget = self.field.widget

        if self.field.localize:
            widget.is_localized = True

        attrs = attrs or {}
        auto_id = self.auto_id
        if auto_id and 'id' not in attrs and 'id' not in widget.attrs:
            if not only_initial:
                attrs['id'] = auto_id
            else:
                attrs['id'] = self.html_initial_id

        if not only_initial:
            name = self.html_name
        else:
            name = self.html_initial_name
        if isinstance( widget, (Widget, MultiWidget, SelectDateWidget,)  ):
            return widget.render(name, self.value(), attrs=attrs, **kwargs)
        else:
            return widget.render(name, self.value(), attrs=attrs, )


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

    def __getitem__(self, name):
        "Returns a BoundField with the given name."
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError('Key %r not found in Form' % name)
        return BoundField(self, field, name)


class BaseForm(LayoutRenderer, forms.BaseForm):
    pass


class Form(LayoutRenderer, forms.Form):
    pass
