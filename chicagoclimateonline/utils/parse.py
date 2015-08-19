from pyzotero import zotero
#from chicagoclimateonline.references.models import Reference, Author, Tag, Reference_tag, Collections

API_KEY = ''
LIB_ID = '256891'

zot = zotero.Zotero(LIB_ID, 'group', API_KEY)

#initiate first 10 items to look through...
#returns list of dicts
z = zot.top(limit=10)

for item in z:
	to_add = z.pop()
	title = to_add['data']['title']
	doi = to_add['data']['DOI']
	itemType = to_add['data']['itemType']
	extra = to_add['data']['extra']
	seriesText = to_add['data']['seriesText']
	series = to_add['data']['series']
	abstractNote = to_add['data']['abstractNote']
	archive = to_add['data']['archive']
	title = to_add['data']['title']
	ISSN = to_add['data']['ISSN']

	#check to see if any relations at all
	if len(to_add['data']['relations']) != 0:
		relations = to_add['data']['relations']


	archiveLocation = to_add['data']['archiveLocation']
	version = to_add['data']['version']
	
	#check to see if there are any keys in 'collections' list
	if len(to_add['data']['collections']) !=0 :
		collections = to_add['data']['collections']

	journalAbbreviation = to_add['data']['journalAbbreviation']
	issue = to_add['data']['issue']
	dateModified = to_add['data']['dateModified']
	seriesTitle = to_add['data']['seriesTitle']
	dateAdded = to_add['data']['dateAdded']

	#check to if any tags in ['tags'] list
	if len(to_add['data']['tags']) != 0:
		tags = to_add['data']['tags']


	accessDate = to_add['data']['accessDate']
	libraryCatalog = to_add['data']['libraryCatalog']
	volume = to_add['data']['volume']
	callNumber =to_add['data']['callNumber']
	key = to_add['data']['key']
	date = to_add['data']['date']
	pages = to_add['data']['pages']
	shortTitle = to_add['data']['shortTitle']
	language = to_add['data']['language']
	rights = to_add['data']['rights']
	url = to_add['data']['url']
	publicationTitle = to_add['data']['publicationTitle']

	creators = to_add['data']['creators']
	for i in range(len(creators)):
		last_name = creators[i]['lastName']
		fisr_name = creators[i]['firstName']

#iterates the original zot.top(limit=10)
#raises error when it can't pull anymore items	
zot.follow()	
