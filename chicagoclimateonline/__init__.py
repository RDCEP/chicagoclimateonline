import random
import re
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from flask import Flask, render_template, g
from flask.ext.pagedown import PageDown
from flask.ext.assets import Environment, Bundle
from flask.ext.cache import Cache
from chicagoclimateonline.filters import safe_markdown, format_currency, \
    search_markdown, smartypants, nbsp
from chicagoclimateonline.constants import BASE_DIR


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['markdown'] = safe_markdown
app.jinja_env.filters['search_markdown'] = search_markdown
app.jinja_env.filters['format_currency'] = format_currency
app.jinja_env.filters['smartypants'] = smartypants
app.jinja_env.filters['nbsp'] = nbsp
app.url_map.strict_slashes = False

cache = Cache(app)

engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True,
    pool_size=10)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))


class C2OBase(object):
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return re.sub(r'(.)([A-Z])', r'\1_\2', cls.__name__).lower()


Base = declarative_base(cls=C2OBase)
Base.query = db_session.query_property()


pagedown = PageDown(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(403)
def not_found(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(500)
def not_found(error):
    return render_template('errors/500.html'), 500


# Load and register Blueprints
# from chicagoclimateonline.references.views import mod as redirect_module
# app.register_blueprint(redirect_module)

# try:
#     from obstructures.search.views import mod as search_module
#     app.register_blueprint(search_module)
# except:
#     pass

from chicagoclimateonline.views import mod as chicagoclimateonline_module
app.register_blueprint(chicagoclimateonline_module)


@app.before_request
def before_request():
    g.db = engine.dispose()


@app.teardown_request
@app.teardown_appcontext
def shutdown_session(exception=None):
    try:
        g.db.close()
        db_session.remove()
    except:
        try:
            db_session.rollback()
            db_session.close()
            g.db.close()
        except:
            pass


assets = Environment(app)
css = Bundle('css/main.css', filters='cssmin', output='gen/main.css')
assets.register('css_main', css)