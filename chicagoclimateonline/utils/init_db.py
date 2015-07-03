import psycopg2
from chicagoclimateonline import engine, Base, db_session
from chicagoclimateonline.constants import BASE_DIR
from chicagoclimateonline.references.models import Tag, Reference, Author


conn = psycopg2.connect("dbname='chicagoclimateonline_001D' user='chicagoclimateonline' host='localhost'")
cur = conn.cursor()


def init_db():
    from chicagoclimateonline.references.models import Base

    try:
        engine.execute('DROP VIEW search')
    except:
        pass

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_data():
    # cur.execute("""DELETE FROM tag""")

    r = Reference(
        type='book',
        title='Solar shit',
        year=2014,
        publish='t',
        # author=a,
    )
    db_session.add(r)

    for tag in (u'energy', u'solar'):
        t = Tag(
            name=tag,
        )
        db_session.add(t)
        r.tags.append(t)

    a = Author(
        first_name='Nate',
        last_name='Matteson',
    )
    db_session.add(a)
    r.author.append(a)

    # r.tags = tags






    db_session.commit()


if __name__ == '__main__':
    # init_db()
    test_data()