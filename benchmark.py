"""
Compares the rendering speed between Django forms and django-floppyforms
"""
import timeit

django = """from django import forms

class DjangoForm(forms.Form):
    text = forms.CharField()
    slug = forms.SlugField()
    some_bool = forms.BooleanField()
    email = forms.EmailField()
    date = forms.DateTimeField()
    file_ = forms.FileField()

rendered = DjangoForm().as_p()"""

flop = """import floppyforms as forms

class FloppyForm(forms.Form):
    text = forms.CharField()
    slug = forms.SlugField()
    some_bool = forms.BooleanField()
    email = forms.EmailField()
    date = forms.DateTimeField()
    file_ = forms.FileField()

rendered = FloppyForm().as_p()"""

def time(stmt):
    t = timeit.Timer(stmt=stmt)
    return t.timeit(number=1000)

print "Plain Django:", time(django)
print "Django-floppyforms:", time(flop)
