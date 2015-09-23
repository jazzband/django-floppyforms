from contextlib import contextmanager

import django
from django.template import Context

try:
    from django.utils.datastructures import MultiValueDict, MergeDict
    MULTIVALUE_DICT_TYPES = (MultiValueDict, MergeDict)
except ImportError:
    # Django >= 1.9
    from django.utils.datastructures import MultiValueDict
    MULTIVALUE_DICT_TYPES = (MultiValueDict,)


REQUIRED_CONTEXT_ATTRIBTUES = (
    '_form_config',
    '_form_render',
)


# We need a custom subclass of dict here in order to allow setting attributes
# on it like _form_config and _form_render.
class DictContext(dict):
    pass


if django.VERSION < (1, 8):
    def get_template(context, template_name):
        from django.template.loader import get_template
        return get_template(template_name)

    def get_context(context):
        # Django < 1.8 only wants ``Context`` instances as context, no dict
        # instances.
        if not isinstance(context, Context):
            context = Context(context)
        return context

else:
    def get_template(context, template_name):
        # Django 1.8 and higher support multiple template engines. We need to
        # load child templates used in the floppyform template tags from the
        # same engine. Otherwise this might get really confusing.
        return context.template.engine.get_template(template_name)

    def get_context(context):
        # Django 1.8 only wants dicts as context, no ``Context`` instances.
        return context


def flatten_context(context):
    if isinstance(context, Context):
        flat = {}
        for d in context.dicts:
            flat.update(d)
        return flat
    else:
        return context


def flatten_contexts(*contexts):
    """Takes a list of context instances and returns a new dict that
    combines all of them."""
    new_context = DictContext()
    for context in contexts:
        if context is not None:
            new_context.update(flatten_context(context))
            for attr in REQUIRED_CONTEXT_ATTRIBTUES:
                if hasattr(context, attr):
                    setattr(new_context, attr, getattr(context, attr))
    return new_context


@contextmanager
def render_context(context_instance, context):
    if context_instance is not None:
        with context_instance.push(context):
            yield context_instance
    else:
        yield get_context(context)
