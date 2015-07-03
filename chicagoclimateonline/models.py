from datetime import datetime
from slugify import slugify
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, \
    Table, Text, Index
from sqlalchemy import event, DDL
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import TSVECTOR
from chicagoclimateonline import Base, engine


class PublishMixin(object):
    publish = Column(Boolean)

    def __init__(self, publish, *args, **kwargs):
        self.publish = publish


class SlugMixin(object):
    name = Column(String(100))
    slug = Column(String(100))

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.slug = slugify(name)

    def __str__(self):
        return self.__class__

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

class DateMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)


class OrderMixin(object):
    order = Column(Integer, default=0)

    def __init__(self, order, *args, **kwargs):
        self.order = order


class PhotoMixin(object):
    width = Column(Integer)
    height = Column(Integer)

    def __init__(self, width, height, *args, **kwargs):
        self.width = width
        self.height = height


class TextMixin(object):
    text = Column(Text)

    def __init__(self, text, *args, **kwargs):
        self.text = text


class PersonMixin(object):
    first_name = Column(String(200))
    last_name = Column(String(200))

    def __init__(self, first_name, last_name, *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def slug(self):
        return slugify('{} {}'.format(self.first_name, self.last_name))

    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class SearchMixin(object):
    search_vector = Column(TSVECTOR)

    @declared_attr
    def __table_args__(self):
        return (
            Index(
                '{}_search_index'.format(self.__name__),
                'search_vector',
                postgresql_using = 'gin'
            ),
        )


class Search(Base):
    # __table__ = Table('search', Base.metadata,
    #     Column('id', Integer, primary_key=True),
    #     autoload=True, autoload_with=engine
    # )
    pass


trigger_snippet = DDL("""
CREATE TRIGGER faq_search_update
    BEFORE UPDATE OR INSERT
    ON faq
    FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger('search_vector', 'pg_catalog.english', 'text', 'question')
""")
