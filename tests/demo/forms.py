import floppyforms as forms
from floppyforms import gis


try:
    import django.contrib.gis.forms as gis_forms
except ImportError:
    gis_forms = None


ALPHA_CHOICES = [
    (c, c.upper())
    for c in 'abcdefhijklmnopqrstuvwxyz'
]

NUMERIC_CHOICES = [
    (c, str(c))
    for c in range(10)
]


def mixin(*classes):
    return type(
        ''.join(cls.__name__ for cls in classes),
        tuple(classes),
        {})


class BaseGMapWidget(gis.BaseGMapWidget):
    # Paste your own Google Maps API key here to test the widgets out.
    google_maps_api_key = None


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

    # GIS fields.
    if gis_forms:
        osm_point = gis.PointField(widget=mixin(gis.PointWidget, gis.BaseOsmWidget))
        osm_multipoint = gis.MultiPointField(widget=mixin(gis.MultiPointWidget, gis.BaseOsmWidget))
        osm_linestring = gis.LineStringField(widget=mixin(gis.LineStringWidget, gis.BaseOsmWidget))
        osm_multilinestring = gis.MultiLineStringField(widget=mixin(gis.MultiLineStringWidget, gis.BaseOsmWidget))
        osm_polygon = gis.PolygonField(widget=mixin(gis.PolygonWidget, gis.BaseOsmWidget))
        osm_multipolygon = gis.MultiPolygonField(widget=mixin(gis.MultiPolygonWidget, gis.BaseOsmWidget))

        gmap_point = gis.PointField(widget=mixin(gis.PointWidget, BaseGMapWidget))
        gmap_multipoint = gis.MultiPointField(widget=mixin(gis.MultiPointWidget, BaseGMapWidget))
        gmap_linestring = gis.LineStringField(widget=mixin(gis.LineStringWidget, BaseGMapWidget))
        gmap_multilinestring = gis.MultiLineStringField(widget=mixin(gis.MultiLineStringWidget, BaseGMapWidget))
        gmap_polygon = gis.PolygonField(widget=mixin(gis.PolygonWidget, BaseGMapWidget))
        gmap_multipolygon = gis.MultiPolygonField(widget=mixin(gis.MultiPolygonWidget, BaseGMapWidget))
