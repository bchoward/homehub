from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
#Base.query = session.query_property() # needed by flask.ext.login
def base_repr(self):
    data = {}
    for key in self.__table__.columns.keys():
        attr = getattr(self, key, None)
        if attr:
            attr = repr(attr)
        data[key] = attr
    key_vals = ' '.join(['%s="%s"' % (k, v) for k,v in data.items()])
    return "<%s.%s: %s> object at 0x%s" % (
        self.__module__, self.__class__.__name__, key_vals, id(self)
    )


Base.__repr__ = base_repr



