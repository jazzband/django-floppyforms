try:
    from django.contrib.gis.forms import GeometryField as BaseGeometryField
except ImportError:
    from floppyforms.fields import CharField as BaseGeometryField

import floppyforms as forms

from floppyforms.gis import widgets

__all__ = ('GeometryField', 'GeometryCollectionField',
           'PointField', 'MultiPointField',
           'LineStringField', 'MultiLineStringField',
           'PolygonField', 'MultiPolygonField')


class GeometryWidget(widgets.BaseMetacartaWidget, widgets.GeometryWidget):
    pass


class GeometryField(BaseGeometryField):
    widget = GeometryWidget

    def __init__(self, *args, **kwargs):
        super(GeometryField, self).__init__(*args, **kwargs)
        self.widget.is_required = self.required  # Django < 1.3 support


class GeometryCollectionWidget(widgets.BaseMetacartaWidget,
                               widgets.GeometryCollectionWidget):
    pass


class GeometryCollectionField(GeometryField):
    widget = GeometryCollectionWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'GEOMETRYCOLLECTION'
        super(GeometryCollectionField, self).__init__(*args, **kwargs)


class PointWidget(widgets.BaseMetacartaWidget, widgets.PointWidget):
    pass


class PointField(GeometryField):
    widget = PointWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'POINT'
        super(PointField, self).__init__(*args, **kwargs)


class MultiPointWidget(widgets.BaseMetacartaWidget, widgets.MultiPointWidget):
    pass


class MultiPointField(GeometryField):
    widget = MultiPointWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'MULTIPOINT'
        super(MultiPointField, self).__init__(*args, **kwargs)


class LineStringWidget(widgets.BaseMetacartaWidget, widgets.LineStringWidget):
    pass


class LineStringField(GeometryField):
    widget = LineStringWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'LINESTRING'
        super(LineStringField, self).__init__(*args, **kwargs)


class MultiLineStringWidget(widgets.BaseMetacartaWidget,
                            widgets.MultiLineStringWidget):
    pass


class MultiLineStringField(GeometryField):
    widget = MultiLineStringWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'MULTILINESTRING'
        super(MultiLineStringField, self).__init__(*args, **kwargs)


class PolygonWidget(widgets.BaseMetacartaWidget, widgets.PolygonWidget):
    pass


class PolygonField(GeometryField):
    widget = PolygonWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'POLYGON'
        super(PolygonField, self).__init__(*args, **kwargs)


class MultiPolygonWidget(widgets.BaseMetacartaWidget,
                         widgets.MultiPolygonWidget):
    pass


class MultiPolygonField(GeometryField):
    widget = MultiPolygonWidget

    def __init__(self, *args, **kwargs):
        kwargs['geom_type'] = 'MULTIPOLYGON'
        super(MultiPolygonField, self).__init__(*args, **kwargs)
