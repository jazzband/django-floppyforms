import difflib
from copy import copy

from django.test import TestCase
from django.test.signals import template_rendered
from django.test.utils import ContextList
from django.utils.unittest.util import safe_repr

from .html import HTMLParseError, parse_html


class InvalidVariable(unicode):
    def __nonzero__(self):
        return False


class _AssertTemplateUsedContext(object):
    def __init__(self, test_case, template_name):
        self.test_case = test_case
        self.template_name = template_name
        self.rendered_templates = []
        self.rendered_template_names = []
        self.context = ContextList()

    def on_template_render(self, sender, signal, template, context, **kwargs):
        self.rendered_templates.append(template)
        self.rendered_template_names.append(template.name)
        self.context.append(copy(context))

    def test(self):
        return self.template_name in self.rendered_template_names

    def message(self):
        return u'%s was not rendered.' % self.template_name

    def __enter__(self):
        template_rendered.connect(self.on_template_render)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        template_rendered.disconnect(self.on_template_render)
        if exc_type is not None:
            return

        if not self.test():
            message = self.message()
            if len(self.rendered_templates) == 0:
                message += u' No template was rendered.'
            else:
                message += u' Following templates were rendered: %s' % (
                    ', '.join(self.rendered_template_names))
            self.test_case.fail(message)


class _AssertTemplateNotUsedContext(_AssertTemplateUsedContext):
    def test(self):
        return self.template_name not in self.rendered_template_names

    def message(self):
        return u'%s was rendered.' % self.template_name


class TemplatesTestCase(object):
    def assertTemplateUsed(self, response=None, template_name=None, msg_prefix=''):
        """
        Asserts that the template with the provided name was used in rendering
        the response. Also usable as context manager.
        """
        if response is None and template_name is None:
            raise TypeError(u'response and/or template_name argument must be provided')

        if msg_prefix:
            msg_prefix += ": "

        # Use assertTemplateUsed as context manager.
        if not hasattr(response, 'templates') or (response is None and template_name):
            if response:
                template_name = response
                response = None
            context = _AssertTemplateUsedContext(self, template_name)
            return context

        template_names = [t.name for t in response.templates]
        if not template_names:
            self.fail(msg_prefix + "No templates used to render the response")
        self.assertTrue(
            template_name in template_names,
            msg_prefix + "Template '%s' was not a template used to render"
            " the response. Actual template(s) used: %s" %
            (template_name, u', '.join(template_names))
        )

    def assertTemplateNotUsed(self, response=None, template_name=None, msg_prefix=''):
        """
        Asserts that the template with the provided name was NOT used in
        rendering the response. Also usable as context manager.
        """
        if response is None and template_name is None:
            raise TypeError(u'response and/or template_name argument must be provided')

        if msg_prefix:
            msg_prefix += ": "

        # Use assertTemplateUsed as context manager.
        if not hasattr(response, 'templates') or (response is None and template_name):
            if response:
                template_name = response
                response = None
            context = _AssertTemplateNotUsedContext(self, template_name)
            return context

        template_names = [t.name for t in response.templates]
        self.assertFalse(
            template_name in template_names,
            msg_prefix + "Template '%s' was used unexpectedly in rendering"
            " the response" % template_name)


def assert_and_parse_html(self, html, user_msg, msg):
    try:
        dom = parse_html(html)
    except HTMLParseError, e:
        standardMsg = u'%s\n%s' % (msg, e.msg)
        self.fail(self._formatMessage(user_msg, standardMsg))
    return dom


class HTMLTestCase(object):
    def assertHTMLEqual(self, html1, html2, msg=None):
        """
        Asserts that two HTML snippets are semantically the same.
        Whitespace in most cases is ignored, and attribute ordering is not
        significant. The passed-in arguments must be valid HTML.
        """
        dom1 = assert_and_parse_html(self, html1, msg,
                                     u'First argument is not valid HTML:')
        dom2 = assert_and_parse_html(self, html2, msg,
                                     u'Second argument is not valid HTML:')

        if dom1 != dom2:
            standardMsg = '%s != %s' % (
                safe_repr(dom1, True), safe_repr(dom2, True))
            diff = ('\n' + '\n'.join(difflib.ndiff(
                           unicode(dom1).splitlines(),
                           unicode(dom2).splitlines())))
            standardMsg = self._truncateMessage(standardMsg, diff)
            self.fail(self._formatMessage(msg, standardMsg))

    def assertHTMLNotEqual(self, html1, html2, msg=None):
        """Asserts that two HTML snippets are not semantically equivalent."""
        dom1 = assert_and_parse_html(self, html1, msg,
                                     u'First argument is not valid HTML:')
        dom2 = assert_and_parse_html(self, html2, msg,
                                     u'Second argument is not valid HTML:')

        if dom1 == dom2:
            standardMsg = '%s == %s' % (
                safe_repr(dom1, True), safe_repr(dom2, True))
            self.fail(self._formatMessage(msg, standardMsg))


class FloppyFormsTestCase(HTMLTestCase, TemplatesTestCase, TestCase):
    pass
