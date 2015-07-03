from flask_wtf import Form
from wtforms.widgets import html_params
from wtforms import TextField, SubmitField, FormField, DateTimeField, TextAreaField
from wtforms.fields.html5 import EmailField, URLField
from wtforms.validators import Required, Email, Optional, URL


class RequiredIf(Required):

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


def date_inputs(field, **kwargs):
    kwargs.setdefault('type', 'text')
    field_id = kwargs.pop('id', field.id)
    html = [u'<label>Year<input {}>'.format(html_params(
        id=u'{}_year'.format(field_id),
        type=u'text',
    ))]
    html.append(u'<label>Month<input {}>'.format(html_params(
        id=u'{}_year'.format(field_id),
        type=u'text',
    )))
    html.append(u'<label>Day<input {}>'.format(html_params(
        id=u'{}_year'.format(field_id),
        type=u'text',
    )))
    return u''.join(html)


class BasicInfo(Form):
    title = TextField('Title', id='ref_title', validators=[Required(), ])
    author = TextField('Author', id='ref_author', validators=[Required(), ])
    abstract = TextAreaField('Abstract', id='ref_abstract', validators=[Optional(), ])


class CommonInfo(Form):
    short_title = TextField('Short Title', id='ref_short_title', validators=[Optional(), ])
    url = URLField('URL', id='ref_url', validators=[Optional(), URL(), ])
    accessed = DateTimeField('Accessed', id='ref_accessed', validators=[Optional(), ])
    archive = TextField('Archive', id='ref_archive', validators=[Optional(), ])
    archive_location = TextField('Location in archive', id='ref_archive_location', validators=[Optional(), ])
    library_catalog = TextField('Library catalog', id='ref_library_catalog', validators=[Optional(), ])
    call_number = TextField('Call number', id='ref_call_number', validators=[Optional(), ])
    rights = TextAreaField('Rights', id='ref_rights', validators=[Optional(), ])
    extra = TextAreaField('Extra', id='ref_extra', validators=[Optional(), ])


class BookBaseForm(Form):
    series = TextField('Series', id='ref_series', validators=[Optional(), ])
    series_number = TextField('Series number', id='ref_series_number', validators=[Optional(), ])
    volume = TextField('Volume', id='ref_volume', validators=[Optional(), ])
    number_of_volumes = TextField('Number of volumes', id='ref_number_of_volumes', validators=[Optional(), ])
    edition = TextField('Edition', id='ref_edition', validators=[Optional(), ])
    place = TextField('Place', id='ref_place', validators=[Optional(), ])
    publisher = TextField('Publisher', id='ref_publisher', validators=[Required(), ])
    year = TextField('Date', id='ref_date', validators=[Required(), ])
    # Need year for bibtex, date for zotero
    number_of_pages = TextField('Number of pages', id='ref_number_of_pages', validators=[Optional(), ])
    language = TextField('Language', id='ref_language', validators=[Optional(), ])
    isbn = TextField('ISBN', id='ref_isbn', validators=[Optional(), ])


class BookForm(Form):
    basic_info = FormField(BasicInfo)
    book_info = FormField(BookBaseForm)
    common_info = FormField(CommonInfo)


class BookSectionForm(Form):
    basic_info = FormField(BasicInfo)
    book_title = TextField('Book title', id='ref_book_title', validators=[Required(), ])
    book_info = FormField(BookBaseForm)
    common_info = FormField(CommonInfo)


class JournalArticleForm(Form):
    basic_info = FormField(BasicInfo)
    publication = TextField('Publication', id='ref_publication',
                            validators=[Required(), ])
    volume = TextField('Volume', id='ref_volume', validators=[Optional(), ])
    issue = TextField('Issue', id='ref_issue', validators=[Optional(), ])
    pages = TextField('Pages', id='ref_pages', validators=[Optional(), ])
    date = TextField('Date', id='ref_date',
                     validators=[Required(), ])
    series = TextField('Series', id='ref_series', validators=[Optional(), ])
    series_title = TextField('Series title', id='ref_series_title',
                             validators=[Optional(), ])
    series_text = TextField('Series text', id='ref_series_text',
                            validators=[Optional(), ])
    journal_abbr = TextField('Journal abbreviation', id='ref_journal_abbr',
                             validators=[Optional(), ])
    language = TextField('Language', id='ref_language',
                         validators=[Optional(), ])
    doi = TextField('DOI', id='ref_doi', validators=[Optional(), ])
    issn = TextField('ISSN', id='ref_issn', validators=[Optional(), ])
    common_info = FormField(CommonInfo)


class ConferencePaperForm(Form):
    basic_info = FormField(BasicInfo)
    proceedings_title = TextField('Proceedings title', id='ref_proceedings_title', validators=[Optional(), ])
    conference_name = TextField('Conference name', id='ref_conference_name', validators=[Optional(), ])
    place = TextField('Place', id='ref_place', validators=[Optional(), ])
    publisher = TextField('Publisher', id='ref_publisher', validators=[Optional(), ])
    volume = TextField('Volume', id='ref_volume', validators=[Optional(), ])
    pages = TextField('Pages', id='ref_pages', validators=[Optional(), ])
    series = TextField('Series', id='ref_series', validators=[Optional(), ])
    language = TextField('Language', id='ref_language', validators=[Optional(), ])
    doi = TextField('DOI', id='ref_doi', validators=[Optional(), ])
    isbn = TextField('ISBN', id='ref_isbn', validators=[Optional(), ])
    common_info = FormField(CommonInfo)


class NewspaperArticleForm(Form):
    basic_info = FormField(BasicInfo)
    publication = TextField('Publication', id='ref_publication', validators=[Optional(), ])
    place = TextField('Place', id='ref_place', validators=[Optional(), ])
    edition = TextField('Edition', id='ref_edition', validators=[Optional(), ])
    date = TextField('Date', id='ref_date', validators=[Optional(), ])
    section = TextField('Section', id='ref_section', validators=[Optional(), ])
    pages = TextField('Pages', id='ref_pages', validators=[Optional(), ])
    language = TextField('Language', id='ref_language', validators=[Optional(), ])
    issn = TextField('ISSN', id='ref_issn', validators=[Optional(), ])
    common_info = FormField(CommonInfo)


class MagazineArticleForm(Form):
    basic_info = FormField(BasicInfo)
    publication = TextField('Publication', id='ref_publication', validators=[Optional(), ])
    volume = TextField('Edition', id='ref_volume', validators=[Optional(), ])
    issue = TextField('Issue', id='ref_issue', validators=[Optional(), ])
    date = TextField('Date', id='ref_date', validators=[Optional(), ])
    pages = TextField('Pages', id='ref_pages', validators=[Optional(), ])
    language = TextField('Language', id='ref_language', validators=[Optional(), ])
    issn = TextField('ISSN', id='ref_issn', validators=[Optional(), ])
    common_info = FormField(CommonInfo)


class WebpageForm(Form):
    basic_info = FormField(BasicInfo)
    website_title = TextField('Website title', id='ref_website_title', validators=[Optional(), ])
    website_type = TextField('Website type', id='ref_website_type', validators=[Optional(), ])
    date = TextField('Date', id='ref_date', validators=[Optional(), ])
    common_info = FormField(CommonInfo)


class ReportForm(Form):
    basic_info = FormField(BasicInfo)
    report_number = TextField('Report number', id='ref_report_number', validators=[Optional(), ])
    report_type = TextField('Report type', id='ref_report_type', validators=[Optional(), ])
    series_title = TextField('Series title', id='ref_series_title', validators=[Optional(), ])
    place = TextField('Place', id='ref_place', validators=[Optional(), ])
    institution = TextField('Institution', id='ref_institution', validators=[Optional(), ])
    date = TextField('Date', id='ref_date', validators=[Optional(), ])
    pages = TextField('Pages', id='ref_pages', validators=[Optional(), ])
    language = TextField('Language', id='ref_language', validators=[Optional(), ])
    common_info = FormField(CommonInfo)


class ManuscriptForm(Form):
    basic_info = FormField(BasicInfo)
    manuscript_type = TextField('Manuscript type', id='ref_manuscript_type', validators=[Optional(), ])
    place = TextField('Place', id='ref_place', validators=[Optional(), ])
    date = TextField('Date', id='ref_date', validators=[Optional(), ])
    number_of_pages = TextField('Number of pages', id='ref_number_of_pages', validators=[Optional(), ])
    language = TextField('Language', id='ref_language', validators=[Optional(), ])
    common_info = FormField(CommonInfo)