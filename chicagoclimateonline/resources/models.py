from sqlalchemy import Column, String, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship
from chicagoclimateonline.models import SlugMixin, DateMixin, TextMixin, \
    PublishMixin
from chicagoclimateonline.topics.models import Topic
from chicagoclimateonline import Base


resource_topic_table = Table('reference_author', Base.metadata,
    Column('reference_id', Integer, ForeignKey('resource.id')),
    Column('author_id', Integer, ForeignKey('topic.id'))
)


class WebResource(SlugMixin, DateMixin, TextMixin, PublishMixin, Base):
    url = Column(String(500))
    topics = relationship(Topic,
                          secondary=resource_topic_table,
                          backref='resources')