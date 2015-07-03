import re
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, \
    Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from chicagoclimateonline.models import SlugMixin, DateMixin, PublishMixin
from chicagoclimateonline import Base


reference_author_table = Table('reference_author', Base.metadata,
    Column('reference_id', Integer, ForeignKey('reference.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)

reference_keyword_table = Table('reference_keyword', Base.metadata,
    Column('reference_id', Integer, ForeignKey('reference.id')),
    Column('author_id', Integer, ForeignKey('author.id'))
)

reference_tag_table = Table('reference_tag', Base.metadata,
    Column('reference_id', Integer, ForeignKey('reference.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)


class Tag(SlugMixin, DateMixin, Base):
    pass


class Author(DateMixin, Base):
    first_name = Column(String(500))
    last_name = Column(String(500))

    def initialed_first_name(self):
        return ' '.join([x[0].uppercase() for x in self.first_name.split()])

    def full_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)


class Reference(DateMixin, PublishMixin, Base):
    type = Column(String(100))
    author = relationship(Author,
                          secondary=reference_author_table,
                          backref='references')
    tags = relationship(Tag,
                          secondary=reference_tag_table,
                          backref='references')
    title = Column(String(800))
    short_title = Column(String(500))

    number_of_pages = Column(Integer)
    publisher = Column(String(500))
    place = Column(String(500))

    publication = Column(String(500))
    journal_abbr = Column(String(500))

    book_title = Column(String(500))

    proceedings_title = Column(String(500))
    conference_name = Column(String(500))

    report_number = Column(String(500))
    report_type = Column(String(500))

    institution = Column(String(500))

    website_title = Column(String(500))
    website_type = Column(String(500))

    manuscript_type = Column(String(500))

    # date = Column(String(500))
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

    edition = Column(Integer)
    issue = Column(String(500))
    pages = Column(String(500))
    volume = Column(Integer)
    number_of_volumes = Column(Integer)

    series = Column(String(500))
    series_text = Column(String(500))
    series_title = Column(String(500))
    series_number = Column(Integer)

    section = Column(String(500))

    doi = Column(String(500))
    isbn = Column(String(500))
    issn = Column(String(500))
    url = Column(String(500))

    language = Column(String(500))

    library_catalog = Column(String(500))
    call_number = Column(String(500))
    archive = Column(String(500))
    archive_location = Column(String(500))

    accessed = Column(DateTime)

    abstract = Column(Text)
    rights = Column(Text)
    extra = Column(Text)

    # Audio Recording
    # label = Column(String(500))
    # format = Column(String(500))
    # running_time = Column(String(500))

    # Bill
    # bill_number = Column(String(500))
    # code = Column(String(500))
    # code_volume = Column(String(500))
    # code_pages = Column(String(500))
    # legislative_body = Column(String(500))
    # session = Column(String(500))
    # history = Column(String(500))

    # Case
    # reporter = Column(String(500))
    # reporter_volume = Column(String(500))
    # court = Column(String(500))
    # docket_number = Column(String(500))
    # first_page = Column(String(500))
    # history = Column(String(500))

    # Hearing
    # committee = Column(String(500))
    # document_number = Column(String(500))
    # legislative_body = Column(String(500))
    # session = Column(String(500))
    # history = Column(String(500))

    # Statute
    # code = Column(String(500))
    # code_number = Column(String(500))
    # public_law_number = Column(String(500))



    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'reference'
    }

    @property
    def bibtex(self):
        b = '{bibtex_type}{{{id}\n  '.format(bibtex_type=self.bibtex_type, id=self.id)
        print([(k, v) for k, v in self.__dict__.iteritems()])
        b += '\n  '.join([str(k + '={{{value}}},'.format(value=v))
                          for k, v in self.__dict__.iteritems()
                          if v is not None and k != 'type' and k[0] != '_'])
        b += '\n}\n'
        return b


class Book(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'book'}

    def apa_style(self):
        return '{}. _{}_. {}'

    @property
    def bibtex_type(self):
        return '@book'
    # bibtex_type = '@book'


class BookSection(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'book_section'}


class JournalArticle(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'journal_article'}

    @property
    def bibtex_type(self):
        return '@article'

class ConferencePaper(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'conference_paper'}

    @property
    def bibtex_type(self):
        return '@inproceedings'


class NewspaperArticle(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'newspaper_article'}

    @property
    def bibtex_type(self):
        return '@article'


class MagazineArticle(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'magazine_article'}

    @property
    def bibtex_type(self):
        return '@article'


class Report(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'report'}

    @property
    def bibtex_type(self):
        return '@techreport'


class Manuscript(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'manuscript'}

    @property
    def bibtex_type(self):
        return '@article'


class Webpage(Reference):
    __tablename__ = None
    __mapper_args__ = {'polymorphic_identity': 'webpage'}
