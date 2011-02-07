from django.conf import settings
from django.test import TestCase
from django.utils.functional import wraps

try:
    from django.contrib.gis.geos import GEOSGeometry
except ImportError:
    """GDAL / GEOS not installed. Tests will fail if contrib.gis
    is installed, and will be skipped otherwise"""

try:
    from django.utils import unittest as ut2
    HAS_UT2 = True
except ImportError:
    HAS_UT2 = False

import floppyforms as forms


# Some test data, geometries as OpenLayers serializes them.
# GEOS's WKT reader normalizes them.
# This is a callable to prevent us from getting warnings from the GEOS C api
GEOMETRIES = lambda: {
    'point': GEOSGeometry("""SRID=4326;POINT(9.052734375 42.451171875)"""),
    'multipoint': GEOSGeometry("SRID=4326;MULTIPOINT("
                               "(13.18634033203125 14.504356384277344),"
                               "(13.207969665527 14.490966796875),"
                               "(13.177070617675 14.454917907714))"),
    'linestring': GEOSGeometry("SRID=4326;LINESTRING("
                               "-8.26171875 -0.52734375,"
                               "-7.734375 4.21875,"
                               "6.85546875 3.779296875,"
                               "5.44921875 -3.515625)"),
    'multilinestring': GEOSGeometry("SRID=4326;MULTILINESTRING("
                                    "(-16.435546875 -2.98828125,"
                                    "-17.2265625 2.98828125,"
                                    "-0.703125 3.515625,"
                                    "-1.494140625 -3.33984375),"
                                    "(-8.0859375 -5.9765625,"
                                    "8.525390625 -8.7890625,"
                                    "12.392578125 -0.87890625,"
                                    "10.01953125 7.646484375))"),
    'polygon': GEOSGeometry("SRID=4326;POLYGON("
                            "(-1.669921875 6.240234375,"
                            "-3.8671875 -0.615234375,"
                            "5.9765625 -3.955078125,"
                            "18.193359375 3.955078125,"
                            "9.84375 9.4921875,"
                            "-1.669921875 6.240234375))"),
    'multipolygon': GEOSGeometry("SRID=4326;MULTIPOLYGON("
                                 "((-17.578125 13.095703125,"
                                 "-17.2265625 10.8984375,"
                                 "-13.974609375 10.1953125,"
                                 "-13.359375 12.744140625,"
                                 "-15.732421875 13.7109375,"
                                 "-17.578125 13.095703125)),"
                                 "((-8.525390625 5.537109375,"
                                 "-8.876953125 2.548828125,"
                                 "-5.888671875 1.93359375,"
                                 "-5.09765625 4.21875,"
                                 "-6.064453125 6.240234375,"
                                 "-8.525390625 5.537109375)))"),
    'geometrycollection': GEOSGeometry("SRID=4326;GEOMETRYCOLLECTION("
                                       "POINT(5.625 -0.263671875),"
                                       "POINT(6.767578125 -3.603515625),"
                                       "POINT(8.525390625 0.087890625),"
                                       "POINT(8.0859375 -2.13134765625),"
                                       "LINESTRING("
                                       "6.273193359375 -1.175537109375,"
                                       "5.77880859375 -1.812744140625,"
                                       "7.27294921875 -2.230224609375,"
                                       "7.657470703125 -1.25244140625))"),
}


def _deferredSkip(condition, reason):
    def decorator(test_func):
        if (not (isinstance(test_func, type)
                 and issubclass(test_func, TestCase))):
            @wraps(test_func)
            def skip_wrapper(*args, **kwargs):
                if condition():
                    if HAS_UT2:
                        raise ut2.SkipTest(reason)
                    return True  # Reporting as success but actually skipped
                return test_func(*args, **kwargs)
            test_item = skip_wrapper
        else:
            test_item = test_func
        test_item.__unittest_skip_why__ = reason
        return test_item
    return decorator


def skipUnlessInstalled(app):
    """Skips the test if ``app`` is not installed"""
    condition = lambda: app not in settings.INSTALLED_APPS
    return _deferredSkip(condition, "%s is not installed" % app)


class GisTests(TestCase):
    """Tests for the GeoDjango widgets"""

    def assertMapWidget(self, form_instance):
        """Makes sure the MapWidget js is passed in the form media
        and a MapWidget is actually created"""
        rendered = form_instance.as_p()
        self.assertTrue('new MapWidget(options);' in rendered, rendered)
        js_path = 'floppyforms/js/MapWidget.js'
        self.assertTrue(js_path in str(form_instance.media))

    def assertTextarea(self, wkt, rendered):
        """Makes sure the wkt and a textarea are in the content"""
        self.assertTrue('<textarea ' in rendered, rendered)
        self.assertTrue(' required ' in rendered, rendered)
        self.assertTrue(wkt in rendered, rendered)

    @skipUnlessInstalled('django.contrib.gis')
    def test_point(self):
        class PointForm(forms.Form):
            p = forms.gis.PointField()

        geom = GEOMETRIES()['point']
        data = {'p': geom}
        rendered = PointForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(PointForm(data=data))
        self.assertTrue(PointForm(data=data).is_valid())
        self.assertFalse(PointForm().is_valid())
        invalid = PointForm(data={'p': 'some invalid geom'})
        self.assertFalse(invalid.is_valid())
        self.assertTrue('Invalid geometry value' in str(invalid.errors))

        valid_geoms = ['point']
        invalid_geoms = ['multipoint', 'linestring', 'multilinestring',
                         'polygon', 'multipolygon', 'geometrycollection']
        for valid in valid_geoms:
            data = {'p': GEOMETRIES()[valid].wkt}
            self.assertTrue(PointForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'p': GEOMETRIES()[invalid].wkt}
            self.assertFalse(PointForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_multipoint(self):
        class PointForm(forms.Form):
            p = forms.gis.MultiPointField()

        geom = GEOMETRIES()['multipoint']
        data = {'p': geom}
        rendered = PointForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(PointForm(data=data))
        self.assertTrue(PointForm(data=data).is_valid())

        valid_geoms = ['multipoint']
        invalid_geoms = ['point', 'linestring', 'multilinestring',
                         'polygon', 'multipolygon', 'geometrycollection']
        for valid in valid_geoms:
            data = {'p': GEOMETRIES()[valid].wkt}
            self.assertTrue(PointForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'p': GEOMETRIES()[invalid].wkt}
            self.assertFalse(PointForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_linestring(self):
        class LineStringForm(forms.Form):
            l = forms.gis.LineStringField()

        geom = GEOMETRIES()['linestring']
        data = {'l': geom}
        rendered = LineStringForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(LineStringForm(data=data))
        self.assertTrue(LineStringForm(data=data).is_valid())

        valid_geoms = ['linestring']
        invalid_geoms = ['point', 'multipoint', 'multilinestring',
                         'polygon', 'multipolygon', 'geometrycollection']
        for valid in valid_geoms:
            data = {'l': GEOMETRIES()[valid].wkt}
            self.assertTrue(LineStringForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'l': GEOMETRIES()[invalid].wkt}
            self.assertFalse(LineStringForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_multilinestring(self):
        class LineStringForm(forms.Form):
            l = forms.gis.MultiLineStringField()

        geom = GEOMETRIES()['multilinestring']
        data = {'l': geom}
        rendered = LineStringForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(LineStringForm(data=data))
        self.assertTrue(LineStringForm(data=data).is_valid())

        valid_geoms = ['multilinestring']
        invalid_geoms = ['point', 'multipoint', 'linestring',
                         'polygon', 'multipolygon', 'geometrycollection']
        for valid in valid_geoms:
            data = {'l': GEOMETRIES()[valid].wkt}
            self.assertTrue(LineStringForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'l': GEOMETRIES()[invalid].wkt}
            self.assertFalse(LineStringForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_polygon(self):
        class PolygonForm(forms.Form):
            p = forms.gis.PolygonField()

        geom = GEOMETRIES()['polygon']
        data = {'p': geom}
        rendered = PolygonForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(PolygonForm(data=data))
        self.assertTrue(PolygonForm(data=data).is_valid())

        valid_geoms = ['polygon']
        invalid_geoms = ['point', 'multipoint', 'linestring',
                         'multilinestring', 'multipolygon',
                         'geometrycollection']
        for valid in valid_geoms:
            data = {'p': GEOMETRIES()[valid].wkt}
            self.assertTrue(PolygonForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'p': GEOMETRIES()[invalid].wkt}
            self.assertFalse(PolygonForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_multipolygon(self):
        class PolygonForm(forms.Form):
            p = forms.gis.MultiPolygonField()

        geom = GEOMETRIES()['multipolygon']
        data = {'p': geom}
        rendered = PolygonForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(PolygonForm(data=data))
        self.assertTrue(PolygonForm(data=data).is_valid())

        valid_geoms = ['multipolygon']
        invalid_geoms = ['point', 'multipoint', 'linestring',
                         'multilinestring', 'polygon', 'geometrycollection']
        for valid in valid_geoms:
            data = {'p': GEOMETRIES()[valid].wkt}
            self.assertTrue(PolygonForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'p': GEOMETRIES()[invalid].wkt}
            self.assertFalse(PolygonForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_geometry(self):
        class GeometryForm(forms.Form):
            g = forms.gis.GeometryField()

        geom = GEOMETRIES()['point']
        data = {'g': geom}
        rendered = GeometryForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(GeometryForm(data=data))
        self.assertTrue(GeometryForm(data=data).is_valid())

        # GeometryField will accept anything...
        valid_geoms = ['point', 'multipoint', 'linestring', 'multilinestring',
                       'polygon', 'multipolygon', 'geometrycollection']
        invalid_geoms = []
        for valid in valid_geoms:
            data = {'g': GEOMETRIES()[valid].wkt}
            self.assertTrue(GeometryForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'g': GEOMETRIES()[invalid].wkt}
            self.assertFalse(GeometryForm(data=data).is_valid())

    @skipUnlessInstalled('django.contrib.gis')
    def test_geometrycollection(self):
        class GeometryForm(forms.Form):
            g = forms.gis.GeometryCollectionField()

        geom = GEOMETRIES()['geometrycollection']
        data = {'g': geom}
        rendered = GeometryForm(data=data).as_p()
        self.assertTextarea(geom.wkt, rendered)
        self.assertMapWidget(GeometryForm(data=data))
        self.assertTrue(GeometryForm(data=data).is_valid())
        self.assertFalse(GeometryForm(data={'g': 'bah'}).is_valid())

        valid_geoms = ['geometrycollection']
        invalid_geoms = ['point', 'multipoint', 'linestring',
                         'multilinestring', 'polygon', 'multipolygon']
        for valid in valid_geoms:
            data = {'g': GEOMETRIES()[valid].wkt}
            self.assertTrue(GeometryForm(data=data).is_valid())

        for invalid in invalid_geoms:
            data = {'g': GEOMETRIES()[invalid].wkt}
            self.assertFalse(GeometryForm(data=data).is_valid())
