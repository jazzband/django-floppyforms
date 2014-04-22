from decimal import Decimal
import django
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import six
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.unittest import expectedFailure, skipIf

import floppyforms as forms

from .models import Registration, AllFields


class RegistrationForm(forms.Form):
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    firstname = forms.CharField(label=_(u'Your first name?'))
    lastname = forms.CharField(label=_(u'Your last name:'))
    username = forms.CharField(max_length=30)
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text=_(u'Make sure to use a secure password.'),
    )
    password2 = forms.CharField(label=_(u'Retype password'), widget=forms.PasswordInput)
    age = forms.IntegerField(required=False)
    height = forms.DecimalField(localize=True, required=False)
    agree_to_terms = forms.BooleanField()

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise ValidationError(u'Haha, you trapped into the honeypot.')
        return self.cleaned_data['honeypot']

    def clean(self):
        if self.errors:
            raise ValidationError(u'Please correct the errors below.')


class RegistrationModelForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = (
            'firstname',
            'lastname',
            'username',
            'age',
        )


class FormRenderAsMethodsTests(TestCase):
    def test_default_rendering(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/default.html'):
            with self.assertTemplateUsed('floppyforms/layouts/table.html'):
                rendered = six.text_type(form)
                self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/default.html'):
            with self.assertTemplateUsed('floppyforms/layouts/table.html'):
                rendered = six.text_type(form)
                self.assertTrue(' name="firstname"' in rendered)

    def test_as_p(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/p.html'):
            rendered = form.as_p()
            self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/p.html'):
            rendered = form.as_p()
            self.assertTrue(' name="firstname"' in rendered)

    def test_as_table(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/table.html'):
            rendered = form.as_table()
            self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/table.html'):
            rendered = form.as_table()
            self.assertTrue(' name="firstname"' in rendered)

    def test_as_ul(self):
        form = RegistrationForm()
        with self.assertTemplateUsed('floppyforms/layouts/ul.html'):
            rendered = form.as_ul()
            self.assertTrue(' name="firstname"' in rendered)

        form = RegistrationModelForm()
        with self.assertTemplateUsed('floppyforms/layouts/ul.html'):
            rendered = form.as_ul()
            self.assertTrue(' name="firstname"' in rendered)


class FormHasChangedTests(TestCase):
    def test_basic_has_changed(self):
        form = RegistrationForm()
        self.assertFalse(form.has_changed())

        form = RegistrationForm({'height': '1.89'})
        self.assertTrue(form.has_changed())

        form = RegistrationForm({'height': '1.89'},
                                initial={'height': Decimal('1.89')})
        self.assertFalse(form.has_changed())

    def test_custom_has_changed_logic_for_checkbox_input(self):
        form = RegistrationForm({'agree_to_terms': True})
        self.assertTrue(form.has_changed())

        form = RegistrationForm({'agree_to_terms': False},
                                initial={'agree_to_terms': False})
        self.assertFalse(form.has_changed())

        form = RegistrationForm({'agree_to_terms': False},
                                initial={'agree_to_terms': 'False'})
        self.assertFalse(form.has_changed())

    @skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
    def test_widgets_do_not_have_has_changed_method(self):
        self.assertFalse(hasattr(forms.CheckboxInput, '_has_changed'))
        self.assertFalse(hasattr(forms.NullBooleanSelect, '_has_changed'))
        self.assertFalse(hasattr(forms.SelectMultiple, '_has_changed'))
        self.assertFalse(hasattr(forms.FileInput, '_has_changed'))
        self.assertFalse(hasattr(forms.DateInput, '_has_changed'))
        self.assertFalse(hasattr(forms.DateTimeInput, '_has_changed'))
        self.assertFalse(hasattr(forms.TimeInput, '_has_changed'))

    def test_has_changed_logic_with_localized_values(self):
        '''
        See: https://code.djangoproject.com/ticket/16612
        '''
        with translation.override('de-de'):
            form = RegistrationForm({'height': '1,89'},
                                    initial={'height': Decimal('1.89')})
            self.assertFalse(form.has_changed())

    if django.VERSION < (1, 6):
        test_has_changed_logic_with_localized_values = expectedFailure(
            test_has_changed_logic_with_localized_values)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class FutureModelFormTests(TestCase):
    def test_auto_boolean(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('boolean',)
        self.assertIsInstance(Form.base_fields['boolean'],
                              forms.BooleanField)

    def test_auto_char(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('char',)
        self.assertIsInstance(Form.base_fields['char'],
                              forms.CharField)

    def test_auto_comma_separated(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('comma_separated',)
        self.assertIsInstance(Form.base_fields['comma_separated'],
                              forms.CharField)

    def test_auto_date(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('date',)
        self.assertIsInstance(Form.base_fields['date'],
                              forms.DateField)

    def test_auto_datetime(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('datetime',)
        self.assertIsInstance(Form.base_fields['datetime'],
                              forms.DateTimeField)

    def test_auto_decimal(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('decimal',)
        self.assertIsInstance(Form.base_fields['decimal'],
                              forms.DecimalField)

    def test_auto_email(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('email',)
        self.assertIsInstance(Form.base_fields['email'],
                              forms.EmailField)

    def test_auto_file_path(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('file_path',)
        self.assertIsInstance(Form.base_fields['file_path'],
                              forms.FilePathField)

    def test_auto_float_field(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('float_field',)
        self.assertIsInstance(Form.base_fields['float_field'],
                              forms.FloatField)

    def test_auto_integer(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('integer',)
        self.assertIsInstance(Form.base_fields['integer'],
                              forms.IntegerField)

    def test_auto_big_integer(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('big_integer',)
        self.assertIsInstance(Form.base_fields['big_integer'],
                              forms.IntegerField)

    def test_auto_ip_address(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('ip_address',)
        self.assertIsInstance(Form.base_fields['ip_address'],
                              forms.IPAddressField)

    def test_auto_generic_ip_address(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('generic_ip_address',)
        self.assertIsInstance(Form.base_fields['generic_ip_address'],
                              forms.GenericIPAddressField)

    def test_auto_null_boolean(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('null_boolean',)
        self.assertIsInstance(Form.base_fields['null_boolean'],
                              forms.NullBooleanField)

    def test_auto_positive_integer(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('positive_integer',)
        self.assertIsInstance(Form.base_fields['positive_integer'],
                              forms.IntegerField)

    def test_auto_positive_small_integer(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('positive_small_integer',)
        self.assertIsInstance(Form.base_fields['positive_small_integer'],
                              forms.IntegerField)

    def test_auto_slug(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('slug',)
        self.assertIsInstance(Form.base_fields['slug'],
                              forms.SlugField)

    def test_auto_small_integer(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('small_integer',)
        self.assertIsInstance(Form.base_fields['small_integer'],
                              forms.IntegerField)

    def test_auto_text(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('text',)
        self.assertIsInstance(Form.base_fields['text'],
                              forms.CharField)
        self.assertIsInstance(Form.base_fields['text'].widget,
                              forms.Textarea)

    def test_auto_time(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('time',)
        self.assertIsInstance(Form.base_fields['time'],
                              forms.TimeField)

    def test_auto_url(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('url',)
        self.assertIsInstance(Form.base_fields['url'],
                              forms.URLField)

    def test_auto_file_field(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('file_field',)
        self.assertIsInstance(Form.base_fields['file_field'],
                              forms.FileField)

    def test_auto_image(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('image',)
        self.assertIsInstance(Form.base_fields['image'],
                              forms.ImageField)

    def test_auto_fk(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('fk',)
        self.assertIsInstance(Form.base_fields['fk'],
                              forms.ModelChoiceField)

    def test_auto_m2m(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('m2m',)
        self.assertIsInstance(Form.base_fields['m2m'],
                              forms.ModelMultipleChoiceField)

    def test_auto_one(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('one',)
        self.assertIsInstance(Form.base_fields['one'],
                              forms.ModelChoiceField)

    def test_auto_choices(self):
        import floppyforms.__future__ as forms

        class Form(forms.ModelForm):
            class Meta:
                model = AllFields
                fields = ('choices',)
        self.assertIsInstance(Form.base_fields['choices'],
                              forms.TypedChoiceField)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class FutureModelFormFactoryTests(TestCase):
    def test_auto_boolean(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('boolean',))
        self.assertIsInstance(form_class.base_fields['boolean'],
                              forms.BooleanField)

    def test_auto_char(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('char',))
        self.assertIsInstance(form_class.base_fields['char'],
                              forms.CharField)

    def test_auto_comma_separated(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('comma_separated',))
        self.assertIsInstance(form_class.base_fields['comma_separated'],
                              forms.CharField)

    def test_auto_date(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('date',))
        self.assertIsInstance(form_class.base_fields['date'],
                              forms.DateField)

    def test_auto_datetime(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('datetime',))
        self.assertIsInstance(form_class.base_fields['datetime'],
                              forms.DateTimeField)

    def test_auto_decimal(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('decimal',))
        self.assertIsInstance(form_class.base_fields['decimal'],
                              forms.DecimalField)

    def test_auto_email(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('email',))
        self.assertIsInstance(form_class.base_fields['email'],
                              forms.EmailField)

    def test_auto_file_path(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('file_path',))
        self.assertIsInstance(form_class.base_fields['file_path'],
                              forms.FilePathField)

    def test_auto_float_field(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('float_field',))
        self.assertIsInstance(form_class.base_fields['float_field'],
                              forms.FloatField)

    def test_auto_integer(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('integer',))
        self.assertIsInstance(form_class.base_fields['integer'],
                              forms.IntegerField)

    def test_auto_big_integer(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('big_integer',))
        self.assertIsInstance(form_class.base_fields['big_integer'],
                              forms.IntegerField)

    def test_auto_ip_address(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('ip_address',))
        self.assertIsInstance(form_class.base_fields['ip_address'],
                              forms.IPAddressField)

    def test_auto_generic_ip_address(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('generic_ip_address',))
        self.assertIsInstance(form_class.base_fields['generic_ip_address'],
                              forms.GenericIPAddressField)

    def test_auto_null_boolean(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('null_boolean',))
        self.assertIsInstance(form_class.base_fields['null_boolean'],
                              forms.NullBooleanField)

    def test_auto_positive_integer(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('positive_integer',))
        self.assertIsInstance(form_class.base_fields['positive_integer'],
                              forms.IntegerField)

    def test_auto_positive_small_integer(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('positive_small_integer',))
        self.assertIsInstance(form_class.base_fields['positive_small_integer'],
                              forms.IntegerField)

    def test_auto_slug(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('slug',))
        self.assertIsInstance(form_class.base_fields['slug'],
                              forms.SlugField)

    def test_auto_small_integer(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('small_integer',))
        self.assertIsInstance(form_class.base_fields['small_integer'],
                              forms.IntegerField)

    def test_auto_text(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('text',))
        self.assertIsInstance(form_class.base_fields['text'],
                              forms.CharField)
        self.assertIsInstance(form_class.base_fields['text'].widget,
                              forms.Textarea)

    def test_auto_time(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('time',))
        self.assertIsInstance(form_class.base_fields['time'],
                              forms.TimeField)

    def test_auto_url(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('url',))
        self.assertIsInstance(form_class.base_fields['url'],
                              forms.URLField)

    def test_auto_file_field(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('file_field',))
        self.assertIsInstance(form_class.base_fields['file_field'],
                              forms.FileField)

    def test_auto_image(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('image',))
        self.assertIsInstance(form_class.base_fields['image'],
                              forms.ImageField)

    def test_auto_fk(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('fk',))
        self.assertIsInstance(form_class.base_fields['fk'],
                              forms.ModelChoiceField)

    def test_auto_m2m(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('m2m',))
        self.assertIsInstance(form_class.base_fields['m2m'],
                              forms.ModelMultipleChoiceField)

    def test_auto_one(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('one',))
        self.assertIsInstance(form_class.base_fields['one'],
                              forms.ModelChoiceField)

    def test_auto_choices(self):
        from floppyforms.__future__.models import modelform_factory

        form_class = modelform_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('choices',))
        self.assertIsInstance(form_class.base_fields['choices'],
                              forms.TypedChoiceField)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class FutureModelFormSetFactoryTests(TestCase):
    def test_auto_boolean(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('boolean',))
        self.assertIsInstance(formset.form.base_fields['boolean'],
                              forms.BooleanField)

    def test_auto_char(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('char',))
        self.assertIsInstance(formset.form.base_fields['char'],
                              forms.CharField)

    def test_auto_comma_separated(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('comma_separated',))
        self.assertIsInstance(formset.form.base_fields['comma_separated'],
                              forms.CharField)

    def test_auto_date(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('date',))
        self.assertIsInstance(formset.form.base_fields['date'],
                              forms.DateField)

    def test_auto_datetime(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('datetime',))
        self.assertIsInstance(formset.form.base_fields['datetime'],
                              forms.DateTimeField)

    def test_auto_decimal(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('decimal',))
        self.assertIsInstance(formset.form.base_fields['decimal'],
                              forms.DecimalField)

    def test_auto_email(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('email',))
        self.assertIsInstance(formset.form.base_fields['email'],
                              forms.EmailField)

    def test_auto_file_path(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('file_path',))
        self.assertIsInstance(formset.form.base_fields['file_path'],
                              forms.FilePathField)

    def test_auto_float_field(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('float_field',))
        self.assertIsInstance(formset.form.base_fields['float_field'],
                              forms.FloatField)

    def test_auto_integer(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('integer',))
        self.assertIsInstance(formset.form.base_fields['integer'],
                              forms.IntegerField)

    def test_auto_big_integer(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('big_integer',))
        self.assertIsInstance(formset.form.base_fields['big_integer'],
                              forms.IntegerField)

    def test_auto_ip_address(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('ip_address',))
        self.assertIsInstance(formset.form.base_fields['ip_address'],
                              forms.IPAddressField)

    def test_auto_generic_ip_address(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('generic_ip_address',))
        self.assertIsInstance(formset.form.base_fields['generic_ip_address'],
                              forms.GenericIPAddressField)

    def test_auto_null_boolean(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('null_boolean',))
        self.assertIsInstance(formset.form.base_fields['null_boolean'],
                              forms.NullBooleanField)

    def test_auto_positive_integer(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('positive_integer',))
        self.assertIsInstance(formset.form.base_fields['positive_integer'],
                              forms.IntegerField)

    def test_auto_positive_small_integer(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('positive_small_integer',))
        self.assertIsInstance(formset.form.base_fields['positive_small_integer'],
                              forms.IntegerField)

    def test_auto_slug(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('slug',))
        self.assertIsInstance(formset.form.base_fields['slug'],
                              forms.SlugField)

    def test_auto_small_integer(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('small_integer',))
        self.assertIsInstance(formset.form.base_fields['small_integer'],
                              forms.IntegerField)

    def test_auto_text(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('text',))
        self.assertIsInstance(formset.form.base_fields['text'],
                              forms.CharField)
        self.assertIsInstance(formset.form.base_fields['text'].widget,
                              forms.Textarea)

    def test_auto_time(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('time',))
        self.assertIsInstance(formset.form.base_fields['time'],
                              forms.TimeField)

    def test_auto_url(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('url',))
        self.assertIsInstance(formset.form.base_fields['url'],
                              forms.URLField)

    def test_auto_file_field(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('file_field',))
        self.assertIsInstance(formset.form.base_fields['file_field'],
                              forms.FileField)

    def test_auto_image(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('image',))
        self.assertIsInstance(formset.form.base_fields['image'],
                              forms.ImageField)

    def test_auto_fk(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('fk',))
        self.assertIsInstance(formset.form.base_fields['fk'],
                              forms.ModelChoiceField)

    def test_auto_m2m(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('m2m',))
        self.assertIsInstance(formset.form.base_fields['m2m'],
                              forms.ModelMultipleChoiceField)

    def test_auto_one(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('one',))
        self.assertIsInstance(formset.form.base_fields['one'],
                              forms.ModelChoiceField)

    def test_auto_choices(self):
        from floppyforms.__future__ import modelformset_factory

        formset = modelformset_factory(AllFields,
                                       form=forms.ModelForm,
                                       fields=('choices',))
        self.assertIsInstance(formset.form.base_fields['choices'],
                              forms.TypedChoiceField)


@skipIf(django.VERSION < (1, 6), 'Only applies to Django >= 1.6')
class FutureInlineFormSetFactoryTests(TestCase):
    def test_auto_boolean(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('boolean',))
        self.assertIsInstance(formset.form.base_fields['boolean'],
                              forms.BooleanField)

    def test_auto_char(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('char',))
        self.assertIsInstance(formset.form.base_fields['char'],
                              forms.CharField)

    def test_auto_comma_separated(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('comma_separated',))
        self.assertIsInstance(formset.form.base_fields['comma_separated'],
                              forms.CharField)

    def test_auto_date(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('date',))
        self.assertIsInstance(formset.form.base_fields['date'],
                              forms.DateField)

    def test_auto_datetime(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('datetime',))
        self.assertIsInstance(formset.form.base_fields['datetime'],
                              forms.DateTimeField)

    def test_auto_decimal(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('decimal',))
        self.assertIsInstance(formset.form.base_fields['decimal'],
                              forms.DecimalField)

    def test_auto_email(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('email',))
        self.assertIsInstance(formset.form.base_fields['email'],
                              forms.EmailField)

    def test_auto_file_path(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('file_path',))
        self.assertIsInstance(formset.form.base_fields['file_path'],
                              forms.FilePathField)

    def test_auto_float_field(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('float_field',))
        self.assertIsInstance(formset.form.base_fields['float_field'],
                              forms.FloatField)

    def test_auto_integer(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('integer',))
        self.assertIsInstance(formset.form.base_fields['integer'],
                              forms.IntegerField)

    def test_auto_big_integer(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('big_integer',))
        self.assertIsInstance(formset.form.base_fields['big_integer'],
                              forms.IntegerField)

    def test_auto_ip_address(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('ip_address',))
        self.assertIsInstance(formset.form.base_fields['ip_address'],
                              forms.IPAddressField)

    def test_auto_generic_ip_address(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('generic_ip_address',))
        self.assertIsInstance(formset.form.base_fields['generic_ip_address'],
                              forms.GenericIPAddressField)

    def test_auto_null_boolean(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('null_boolean',))
        self.assertIsInstance(formset.form.base_fields['null_boolean'],
                              forms.NullBooleanField)

    def test_auto_positive_integer(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('positive_integer',))
        self.assertIsInstance(formset.form.base_fields['positive_integer'],
                              forms.IntegerField)

    def test_auto_positive_small_integer(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('positive_small_integer',))
        self.assertIsInstance(formset.form.base_fields['positive_small_integer'],
                              forms.IntegerField)

    def test_auto_slug(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('slug',))
        self.assertIsInstance(formset.form.base_fields['slug'],
                              forms.SlugField)

    def test_auto_small_integer(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('small_integer',))
        self.assertIsInstance(formset.form.base_fields['small_integer'],
                              forms.IntegerField)

    def test_auto_text(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('text',))
        self.assertIsInstance(formset.form.base_fields['text'],
                              forms.CharField)
        self.assertIsInstance(formset.form.base_fields['text'].widget,
                              forms.Textarea)

    def test_auto_time(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('time',))
        self.assertIsInstance(formset.form.base_fields['time'],
                              forms.TimeField)

    def test_auto_url(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('url',))
        self.assertIsInstance(formset.form.base_fields['url'],
                              forms.URLField)

    def test_auto_file_field(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('file_field',))
        self.assertIsInstance(formset.form.base_fields['file_field'],
                              forms.FileField)

    def test_auto_image(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('image',))
        self.assertIsInstance(formset.form.base_fields['image'],
                              forms.ImageField)

    def test_auto_fk(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('fk',))
        self.assertIsInstance(formset.form.base_fields['fk'],
                              forms.ModelChoiceField)

    def test_auto_m2m(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('m2m',))
        self.assertIsInstance(formset.form.base_fields['m2m'],
                              forms.ModelMultipleChoiceField)

    def test_auto_one(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('one',))
        self.assertIsInstance(formset.form.base_fields['one'],
                              forms.ModelChoiceField)

    def test_auto_choices(self):
        from floppyforms.__future__ import inlineformset_factory

        formset = inlineformset_factory(Registration, AllFields,
                                        fk_name='fk',
                                        form=forms.ModelForm,
                                        fields=('choices',))
        self.assertIsInstance(formset.form.base_fields['choices'],
                              forms.TypedChoiceField)
