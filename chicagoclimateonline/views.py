from sqlalchemy import func, Unicode
from flask import Blueprint, render_template, request, flash, make_response, \
    url_for
from chicagoclimateonline.forms import SearchForm
from chicagoclimateonline.models import Search
from chicagoclimateonline.constants import SEARCH_MODELS
from chicagoclimateonline import db_session
import chicagoclimateonline


mod = Blueprint('chicagoclimateonline', __name__, static_folder='static')


@mod.route('/')
def index():
    return render_template(
        'index.html',
        home=True,
    )


@mod.route('/search', methods=['GET', 'POST', ])
def search():
    results = []
    form = SearchForm(request.form)
    if form.validate_on_submit():
        search_terms = form.search_terms.data
        q = db_session.query(Search).\
            filter('search.search_vector @@ plainto_tsquery(:terms)')
        q = q.params(terms=search_terms)
        q = q.add_column(func.ts_headline('pg_catalog.english',
                   Search.text,
                   func.plainto_tsquery(search_terms),
                   'MaxFragments=3,FragmentDelimiter=|||,'
                   'StartSel="<span class=""search-highlight"">", '
                   'StopSel = "</span>", ',
                   type_= Unicode))
        q = q.add_column(func.ts_headline('pg_catalog.english',
                   Search.title,
                   func.plainto_tsquery(search_terms),
                   'HighlightAll=TRUE, '
                   'StartSel="<span class=""search-title-highlight"">", '
                   'StopSel = "</span>"',
                   type_= Unicode))
        q = q.order_by(
            'ts_rank_cd(search.search_vector, plainto_tsquery(:terms)) DESC')
        q = q.limit(10)
        results=[{
            'object': db_session.query(getattr(getattr(getattr(
                chicagoclimateonline, SEARCH_MODELS[entry.object]), 'models'),
                entry.object.capitalize())).get(entry.object_id),
            'fragments': fragments.split('|||'),
            'title': title,
            'module': SEARCH_MODELS[entry.object],
            'class': entry.object
        } for entry, fragments, title in q]
        flash('Your results for <b>{}</b>'.format(search_terms))
    else:
        flash('''Terribly sorry, but it seems that there was a problem with
        the search terms you entered.''')
    return render_template(
        'etc/search.html',
        # search_terms=search_terms,
        results=results,
        search_form=form,
    )

