from flask_wtf import Form
from wtforms import TextField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Required, Email


class SearchForm(Form):
    search_terms = TextField('Search Terms', id='search_terms',
                             validators=[Required(), ])
    # submit = SubmitField('&#8617;', id='search_submit')


class MailingListForm(Form):
    email = EmailField('Email', id='mailing_list_email',
                       validators=[Required(), Email(), ],)
    # submit = SubmitField('&#8617;', id='mailing_list_submit')

