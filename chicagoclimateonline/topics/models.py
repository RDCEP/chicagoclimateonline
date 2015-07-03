from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, \
    Table
from sqlalchemy.orm import relationship, backref
from chicagoclimateonline.models import SlugMixin, TextMixin, DateMixin, \
    PublishMixin
from chicagoclimateonline import Base


class Topic(SlugMixin, TextMixin, DateMixin, PublishMixin, Base):
    parent_id = Column(Integer, ForeignKey('topic.id'))
    parent = relationship('Topic', backref=backref('subtopics'))


topic_reference_table = Table('topic_reference', Base.metadata,
    Column('topic_id', Integer, ForeignKey('topic.id')),
    Column('reference_id', Integer, ForeignKey('reference.id'))
)