from django import template


register = template.Library()


@register.inclusion_tag(
    "test_templatetags/test_inclusion_tag.html", takes_context=True)
def test_inclusion_tag(context, variable):
    context.update({'variable': variable})
    return context
