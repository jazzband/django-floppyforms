from floppyforms.forms import Form as FloppyForm
from floppyforms.__future__.models import (ModelFormMetaclass,
                                           ModelForm as FloppyModelForm)
from floppyforms.models import ModelForm as OldFloppyModelForm
import floppyforms.fields as ff_fields
import floppyforms.widgets as ff_widgets

from django.forms import Form as DjangoForm, ModelForm as DjangoModelForm
from django.utils import six
import django

try:
    from collections import OrderedDict
except ImportError:
    # Python 2.6
    from django.utils.datastructures import SortedDict as OrderedDict

import warnings
import inspect

__all__ = ('make_floppy',)


class TestForm(FloppyForm):
    pass


def _get_class_args(klass):
    """
    Returns a list of arguments and dict of keyword arguments which can be
    passed to klass when on instantiation
    """

    klass_args = []
    klass_kwargs = {}

    # Run through the inheritance chain of the class, gathering args and
    # kwargs which are defined on each method. We only use the args
    # signature of the most top level class (which should be the class itself)
    klasses = inspect.getmro(klass)
    for kls in reversed(klasses):  # reverse order to use the most top level
        if (
            not inspect.isfunction(kls.__init__) and  # python 3
            not inspect.ismethod(kls.__init__)  # python 2
        ):
            continue

        # Get the ArgSpec of initialization method
        spec = inspect.getargspec(kls.__init__)
        arg_names = spec[0]

        # remove "self"
        if arg_names:
            arg_names.pop(0)

        if spec.defaults:  # has kwargs
            # kwarg names in arg_names are the last N values,
            # where N is the lenght of defaults
            start_index = len(arg_names) - len(spec.defaults)

            current_index = 0
            for kwarg in arg_names[start_index:]:
                # build a kwarg signature based on the defaults, in order
                klass_kwargs[kwarg] = spec.defaults[current_index]
                current_index += 1

            # the remaining arg names are positional args
            kls_args = arg_names[:start_index]
        else:
            # no kwargs, they're all positional args
            kls_args = arg_names

        # use the positional args from the primary class
        if kls is klass:
            klass_args = kls_args

    return klass_args, klass_kwargs


def _get_calling_args(instance):
    """
    Returns a list of args and dict of keyword args which would be passed to
    instance when creating it
    """

    calling_args = []
    calling_kwargs = {}
    klass = instance.__class__
    klass_args, klass_kwargs = _get_class_args(klass)

    # Positional args are tricky. We hope they're assigned as properties
    # with the same name, and if so, use that value
    for arg_name in klass_args:
        calling_args.append(getattr(instance, arg_name, None))

    # Keyword args likewise are assumed to be properties of the instance
    # using the keyword value
    for key, val in six.iteritems(instance.__dict__):
        if key in klass_kwargs.keys():
            calling_kwargs[key] = val

    return calling_args, calling_kwargs


def make_floppy(form_class):

    if not inspect.isclass(form_class):
        raise TypeError('"make_floppy" should receive a class, not an instance')

    if not issubclass(form_class, (DjangoForm, DjangoModelForm)):
        raise TypeError('"make_floppy" only works on Forms and ModelForms')

    if (issubclass(form_class, (FloppyForm, FloppyModelForm))):
        warnings.warn(
            """Attempting to reclassify an existing\
               Floppyform class as a Floppyform""",
            RuntimeWarning)
        return form_class

    # Depending on which type of form this is, we create a new inheritance
    # chain, which preserves the current chain and includes Floppyforms,
    # so isinstance and issubclass will pass on new class
    if django.VERSION >= (1, 6) and issubclass(form_class,
                                               DjangoModelForm):
        # complying with the __future__ functionality
        class_list = (six.with_metaclass(ModelFormMetaclass,
                                         form_class, FloppyModelForm),)
    else:
        if issubclass(form_class, DjangoModelForm):
            class_list = (form_class, OldFloppyModelForm)
        else:
            class_list = (form_class, FloppyForm)

    # create the new class
    new_form_class = type(form_class.__name__, class_list, {})

    # preserve the module location
    new_form_class.__module__ = form_class.__module__

    # We also need to map the fields over, converting them to Floppyforms
    # fields when possible. Custom fields will need to be converted in
    # implementations

    # In ModelForms, we only care about the declared fields
    if issubclass(new_form_class, DjangoModelForm):
        existing_fields = new_form_class.declared_fields
    else:
        # Regular Forms, we use all fields
        existing_fields = new_form_class.base_fields

    if existing_fields:
        floppy_fields = []

        # Go through all the fields and swap in their Floppyforms equivalent
        for name, field in six.iteritems(form_class.base_fields):
            if hasattr(ff_fields, field.__class__.__name__):
                new_field_class = getattr(ff_fields,
                                          field.__class__.__name__)
            else:
                new_field_class = None
                warnings.warn("Cannot make custom field {field} floppy".format(
                    field=field.__class__.__name__
                ), RuntimeWarning)
            calling_args, calling_kwargs = _get_calling_args(field)

            # If the field was created with a specifically defined widget,
            # try and swap this with the Floppyforms equivalent as well.
            # Like fields, custom widgets will need to be updated by implementors
            widget = calling_kwargs.pop('widget', None)
            if widget:
                if hasattr(ff_widgets, widget.__class__.__name__):
                    new_widget_class = getattr(ff_widgets,
                                               widget.__class__.__name__)
                    w_calling_args, w_calling_kwargs = _get_calling_args(widget)

                    new_widget = new_widget_class(*w_calling_args,
                                                  **w_calling_kwargs)
                    # If we updated the field, update the widget on that field
                    if new_field_class:
                        calling_kwargs['widget'] = new_widget
                    else:
                        # Just update the widget on the existing field
                        field.widget = widget
                else:
                    warnings.warn("Cannot make custom widget {widget} floppy".format(
                        widget=widget.__class__.__name__
                    ), RuntimeWarning)
                    # A new field preserves the same widget in this case
                    if new_field_class:
                        calling_kwargs['widget'] = widget

            # Create the new field if we can
            if new_field_class:
                new_field = new_field_class(*calling_args,
                                            **calling_kwargs)
            else:
                # Reuse the old field if we couldn't update it
                new_field = field
            floppy_fields.append((name, new_field))

        new_fields = OrderedDict(floppy_fields)

        if issubclass(new_form_class, DjangoModelForm):
            new_form_class.declared_fields = new_fields
        else:
            new_form_class.base_fields = new_fields

    return new_form_class
