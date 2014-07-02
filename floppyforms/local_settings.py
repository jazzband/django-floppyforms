# -*- coding: utf-8 -*-

from django.conf import settings

__all__ = ('DEFAULT_WIDGET_TEMPLATES', )


DEFAULT_WIDGET_TEMPLATES = {
    'floppyforms.widgets.Input' : 'floppyforms/input.html',
#     'floppyforms.widgets.TextInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.PasswordInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.HiddenInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.MultipleHiddenInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.SearchInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.RangeInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.ColorInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.EmailInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.URLInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.PhoneNumberInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.NumberInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.IPAddressInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.FileInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.DateInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.DateTimeInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.TimeInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.CheckboxInput' : 'floppyforms/input.html',
#     'floppyforms.widgets.SlugInput' : 'floppyforms/input.html',
    'floppyforms.widgets.ClearableFileInput' : 'floppyforms/clearable_input.html',
    'floppyforms.widgets.Textarea' : 'floppyforms/textarea.html',
    'floppyforms.widgets.Select' : 'floppyforms/select.html',
#     'floppyforms.widgets.NullBooleanSelect' : 'floppyforms/select.html',
#     'floppyforms.widgets.SelectMultiple' : 'floppyforms/select.html',
    'floppyforms.widgets.RadioSelect' : 'floppyforms/radio.html',
    'floppyforms.widgets.CheckboxSelectMultiple' : 'floppyforms/checkbox_select.html',
    'floppyforms.widgets.SelectDateWidget' : 'floppyforms/select_date.html',
    
    'floppyforms.gis.widgets.BaseGeometryWidget' : 'floppyforms/gis/openlayers.html',
    'floppyforms.gis.widgets.BaseOsmWidget' : 'floppyforms/gis/osm.html',
    'floppyforms.gis.widgets.BaseGMapWidget' : 'floppyforms/gis/google.html',
}
DEFAULT_WIDGET_TEMPLATES.update(getattr(settings, 'FLOPPYFORMS_DEFAULT_WIDGET_TEMPLATES', {}))
