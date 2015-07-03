
COMMON_FIELDS = [
    'short_title', 'url', 'accessed', 'archive', 'archive_location',
    'library_catalog', 'call_number', 'rights', 'extra',
]

BOOK_FIELDS = [
    'title', 'author', 'abstract',
    'series', 'series_number', 'volume',
    'number_of_volumes', 'edition', 'place', 'publisher', 'date',
    'number_of_pages', 'language', 'isbn',
] + COMMON_FIELDS

BOOK_SECTION_FIELDS = [
    'title', 'author', 'abstract',
    'book_title',
    'series', 'series_number', 'volume',
    'number_of_volumes', 'edition', 'place', 'publisher', 'date',
    'number_of_pages', 'language', 'isbn',
] + COMMON_FIELDS

JOURNAL_ARTICLE_FIELDS = [
    'title', 'author', 'abstract',
    'publication', 'volume', 'issue',
    'pages', 'date', 'series', 'series_title', 'series_text', 'journal_abbr',
    'language', 'doi', 'issn',
] + COMMON_FIELDS

CONFERENCE_PAPER_FIELDS = [
    'title', 'author', 'abstract',
    'proceedings_title', 'conference_name', 'place', 'publisher',
    'volume', 'pages', 'series', 'language', 'doi', 'isbn',
] + COMMON_FIELDS

NEWSPAPER_ARTICLE_FIELDS = [
    'title', 'author', 'abstract',
    'publication', 'place', 'edition', 'date', 'section', 'pages',
    'language', 'issn',
] + COMMON_FIELDS

MAGAZINE_ARTICLE_FIELDS = [
    'title', 'author', 'abstract',
    'publication', 'volume', 'issue', 'date', 'pages',
    'language', 'issn',
] + COMMON_FIELDS

WEBPAGE_FIELDS = [
    'title', 'author', 'abstract',
    'website_title', 'website_type', 'date',
] + COMMON_FIELDS

REPORT_FIELDS = [
    'title', 'author', 'abstract',
    'report_number', 'report_type', 'series_title', 'place',
    'institution', 'date', 'pages', 'language',
] + COMMON_FIELDS

MANUSCRIPT_FIELDS = [
    'title', 'author', 'abstract',
    'manuscript_type', 'place', 'date',
    'number_of_pages', 'language'
] + COMMON_FIELDS
