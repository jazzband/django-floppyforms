import floppyforms as forms


ALPHA_CHOICES = [
    (c, c.upper())
    for c in 'abcdefhijklmnopqrstuvwxyz'
]

NUMERIC_CHOICES = [
    (c, str(c))
    for c in range(10)
]


class AllFieldsForm(forms.Form):
    boolean = forms.BooleanField()
    char = forms.CharField(max_length=50)
    choices = forms.ChoiceField(choices=ALPHA_CHOICES)
    date = forms.DateField()
    datetime = forms.DateTimeField()
    decimal = forms.DecimalField(decimal_places=2, max_digits=4)
    email = forms.EmailField()
    file_field = forms.FileField()
    file_path = forms.FilePathField(path='uploads/')
    float_field = forms.FloatField()
    generic_ip_address = forms.GenericIPAddressField()
    image = forms.ImageField()
    integer = forms.IntegerField()
    ip_address = forms.IPAddressField()
    multiple_choices = forms.MultipleChoiceField(choices=ALPHA_CHOICES)
    null_boolean = forms.NullBooleanField()
    regex_field = forms.RegexField(regex='^\w+$', js_regex='^[a-zA-Z]+$')
    slug = forms.SlugField()
    split_datetime = forms.SplitDateTimeField()
    time = forms.TimeField()
    typed_choices = forms.TypedChoiceField(choices=NUMERIC_CHOICES, coerce=int)
    typed_multiple_choices = forms.TypedMultipleChoiceField(choices=NUMERIC_CHOICES, coerce=int)
    url = forms.URLField()
