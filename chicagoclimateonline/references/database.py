#! /user/bin/python

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, Text, Float, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, relationship, backref
from chicagoclimateonline.models import SlugMixin, DateMixin, PublishMixin
from chicagoclimateonline import engine, Base, db_session
from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy.sql.expression import *
from chicagoclimateonline import engine
make_searchable()

class Reference(Base,DateMixin, SlugMixin):
	__tablename__ = 'reference'
  
	type = Column(String(500))
	id = Column(Integer, Sequence('seq_reference_id'), primary_key=True)
  
	title = Column(String(800))
	short_title = Column(String(500))
	number_of_pages = Column(Integer)
	publisher = Column(String(500))
	place = Column(String(500))
	abstract = Column(Text)

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
	url = Column(String(500)) 
	rights = Column(Text)
	extra = Column(Text)
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

	#author_id = Column(Integer, ForeignKey(u'author.id'))
	search_vector = Column(TSVectorType)
	
	#__mapper_args__ = {
	#	'polymorphic_on': type,
	#	'polymorphic_identity': 'reference'
	#}


class Author(Base):
	__tablename__ = 'author'

	id = Column(Integer, Sequence('seq_author_id'), primary_key=True)
	first_name = Column(String(500))
	last_name = Column(String(500))

	#reference_id = Column(Integer, ForeignKey(u'reference.id'))  
	#reference = relationship(u'Reference')
	search_vector = Column(TSVectorType)

	#__mapper_args__ = {'polymorphic_identity': 'author'}



class Book(Base):
	__tablename__ = 'book'

	reference_id = Column(Integer, ForeignKey(u'reference.id'))
	reference = relationship(u'Reference')

	__mapper_args__ = {'polymorphic_identity': 'book'}

class article(Base):
	__tablename__ ='article'
  	__mapper_args__ = {'polymorphic_identity': 'article'}
  
class Proceedings(Base):
	__tablename__ = 'proceedings'
	__mapper_args__ = {'polymorphic_identity': 'proceedings'}

class BookSection(Base):
  __tablename__ = 'booksection'
  __mapper_args__ = {'polymorphic_identity': 'book_section'}


class ConferencePaper(Base):
	__tablename__ = 'conference_paper'
	__mapper_args__ = {'polymorphic_identity': 'conference_paper'}

class NewspaperArticle(Base):
	__tablename__ = 'newspaper_article'
	__mapper_args__ = {'polymorphic_identity': 'newspaper_article'}

class MagazineArticle(Base):
	__tablename__ = 'mag_article'
	__mapper_args__ = {'polymorphic_identity': 'magazine_article'}

class Report(Base):
	__tablename__ = 'report'
	__mapper_args__ = {'polymorphic_identity': 'report'}

class Manuscript(Base):
	__tablename__ = 'manuscript'
	__mapper_args__ = {'polymorphic_identity': 'manuscript'}

class Webpage(Base):
	__tablename__ = 'webpage'
	__mapper_args__ = {'polymorphic_identity': 'webpage'}

	url = Column(String(500))
	website_title = Column(String(500))
	website_type = Column(String(500))

class Reference_tag(Base):
	id = Column(Integer, Sequence('seq_reference_tag_id'), primary_key=True)
	reference_id = Column(Integer, ForeignKey(u'reference.id'))
	tag_id = Column(Integer, ForeignKey(u'tags.id'))

class Tag(Base):
	__tablename__ = 'tags'

	id = Column(Integer, Sequence('seq_tags_id'), primary_key=True)
	tag = Column(String(255))
 
class Collections(Base):
	__tablename__ = 'collections'
	id = Column(Integer, Sequence('seq_collections_id'), primary_key=True)
	collection = Column(String(500))


Base.metadata.create_all(engine)

#this is all test data below
from pyzotero import zotero

zot = zotero.Zotero('256891','group','4clrzj5iITsmNymmoEo3ICNu')

to_add = zot.item('6F4UZGJD')

title1 = to_add['data']['title']

DOI1 = to_add['data']['title']

abstract1 = to_add['data']['abstractNote']

itemType1 = to_add['data']['itemType']

author1 = to_add['data']['creators'][0]


citation1 = Reference( title= title1, doi=DOI1, abstract = abstract1, type= itemType1)
citation2 = Author( first_name = author1['firstName'], last_name = author1['lastName'])

db_session.add(citation1)
db_session.add(citation2)
db_session.flush()

 





