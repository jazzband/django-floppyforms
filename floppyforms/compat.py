import django
from django.template import Context


if django.VERSION < (1, 8):
    def get_template(context, template_name):
        from django.template.loader import get_template
        return get_template(template_name)

    def get_context(context):
        # Django < 1.8 only wants ``Context`` instances as context, no dict
        # instances.
        if not isinstance(context, Context):
            return Context(context)
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
