# -*- coding: utf-8 -*-
from django.forms.widgets import Widget

from . import local_settings

__all__ = ('get_template_by_class', )


def get_template_by_class(widget_or_class):
    if isinstance(widget_or_class, Widget):
        widget_or_class = widget_or_class.__class__
    key = "%s.%s" % (widget_or_class.__module__, widget_or_class.__name__, )
    
    template_name = local_settings.DEFAULT_WIDGET_TEMPLATES.get(key, None)
    if template_name is None:
        for base_class in widget_or_class.__bases__:
            if issubclass(base_class, Widget) and base_class <> Widget:
                template_name = get_template_by_class(base_class)
                if template_name is not None:
                    break
    
    return template_name