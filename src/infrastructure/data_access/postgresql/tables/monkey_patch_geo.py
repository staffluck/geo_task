# type: ignore

import geoalchemy2


class Geometry(geoalchemy2.Geometry):
    cache_ok = True

    def column_expression(self, col):  # noqa
        return geoalchemy2.types.func.ST_AsText(col, type_=self)

    def result_processor(self, dialect, col_type):  # noqa
        def process(value):  # noqa
            if value is not None:
                return WKTElement(value, srid=self.srid)

        return process


class WKTElement(geoalchemy2.WKTElement):
    @property
    def coords(self):  # noqa
        st = self.data.replace("POLYGON((", "").replace("))", "")
        return [tuple(map(float, s.split())) for s in st.split(",")]

    @property
    def longitude(self):  # noqa
        st = self.data
        return float(st[st.index("(") + 1 : st.index(" ")])

    @property
    def latitude(self):  # noqa
        st = self.data
        return float(st[st.index(" ") + 1 : len(st) - 1])

    def __nonzero__(self):  # noqa
        return bool(self.data)


geoalchemy2.Geometry = Geometry
geoalchemy2.WKTElement = WKTElement
