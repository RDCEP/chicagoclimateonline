import os
import shutil
import psycopg2
from obstructures.constants import BASE_DIR
from obstructures import db_session, engine, Base
from obstructures.work.models import Project, ProjectImage, ProjectFile, \
    ProjectUrl, ProjectType
# from obstructures.models import Search
from obstructures.shop.models import Product, ProductImage, ProductFile, ProductUrl
from obstructures.people.models import Member, Collaborator, collaborator_project_table
from obstructures.utils.html2text import html2text

COLLABORATOR_ID_MAP = {}
PROJECT_ID_MAP = {}
PRODUCT_ID_MAP = {}
conn = psycopg2.connect("dbname='obstructures' user='obstructures' host='localhost'")
cur = conn.cursor()


def init_db():
    from obstructures.work.models import Base

    try:
        engine.execute('DROP VIEW search')
    except:
        pass

    try:
        engine.execute('DROP TABLE search')
    except:
        pass

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    from obstructures.work.models import ProjectType, ProjectCategory
    from obstructures.constants import PROJECT_TYPES, PROJECT_CATEGORIES

    for category in PROJECT_CATEGORIES:
        cat = ProjectCategory(
            name=category[0],
            order=category[1],
        )
        db_session.add(cat)
        db_session.commit()

    for category_id, project_type in PROJECT_TYPES:
        pt = ProjectType(
            category_id=category_id,
            name=project_type,
        )
        db_session.add(pt)
        db_session.commit()
        # db_session.flush()

    db_session.commit()


def copy_projects():
    # PROJECTS
    cur.execute("""SELECT * from work_project""")
    rows = cur.fetchall()
    for row in rows:
        old_id = row[0]
        print('project:', row[2])
        project = Project(
            publish=True, name=row[2].decode('utf-8'), long_name=row[10].decode('utf-8'),
            year=int(row[6]), category_id=int(row[8]), order=int(row[15]),
            location=row[11].decode('utf-8'), client=row[12].decode('utf-8'),
            award=row[13].decode('utf-8'), thumbnail=None,
            project_type_id=1, text=None # project_type_id=row[9]
        )
        db_session.add(project)
        db_session.flush()

        project.publish = True
        project.order = int(row[15])
        PROJECT_ID_MAP[row[0]] = project.id

        cur.execute("""SELECT * FROM work_projecttext WHERE project_id={}""".format(row[0]))
        try:
            textrow = cur.fetchone()
            project.text = html2text(textrow[1].decode('utf-8'))
        except:
            pass

        thumbnail_path = row[14]
        _rel_dir = os.path.join('images', 'projects', '{}_{}'.format(project.id, project.slug))
        _dir = os.path.join(BASE_DIR, 'static', _rel_dir)
        try:
            os.mkdir(_dir)
            shutil.copy(os.path.join(BASE_DIR, 'static', 'old', thumbnail_path), _dir)
        except OSError:
            pass
        project.thumbnail = os.path.join(_rel_dir, os.path.basename(thumbnail_path))

    # PROJECT IMAGES
        cur.execute("""SELECT * from work_projectimage WHERE project_id={}""".format(row[0]))
        for row in cur.fetchall():
            image_path = str(row[7])
            try:
                shutil.copy(os.path.join(BASE_DIR, 'static', 'old', image_path), _dir)
            except OSError:
                pass
            project_image = ProjectImage(
                publish=True,
                project_id=project.id,
                path=os.path.join(_rel_dir, os.path.basename(image_path)),
                width=row[4],
                height=row[5],
            )
            db_session.add(project_image)
            db_session.flush()
            project_image.publish = True
            project_image.order = int(row[3])

        # cur.execute("""SELECT * from work_projectresource WHERE project_id={}""".format(old_id))
        # for row in cur.fetchall():
        #     project_url = ProjectUrl(
        #         publish=True,
        #         name=row[2].decode('utf-8'),
        #         order=int(row[6]),
        #         project_id=project.id,
        #         url=row[10].decode('utf-8'),
        #     )
        #     db_session.add(project_url)
        #     db_session.flush()
        #     project_url.order = int(row[6])
        #     project_url.publish = True

    db_session.commit()


def copy_itemsforsale():
    # PROJECTS
    cur.execute("""SELECT * from shop_itemforsale""")
    for row in cur.fetchall():
        old_id = row[0]
        print('product:', row[2])
        product = Product(
            publish=True,
            name=row[2].decode('utf-8'),
            long_name=row[8].decode('utf-8'),
            project_id=PROJECT_ID_MAP[row[7]],
            order=int(row[6]),
            paypal_code=row[11],
            thumbnail=None,
            text=None,
            price=row[12],
        )
        db_session.add(product)
        db_session.flush()

        product.order = int(row[6])
        product.publish = True
        PRODUCT_ID_MAP[row[0]] = product.id

        cur.execute("""SELECT * FROM shop_itemforsaletext WHERE item_id={}""".format(row[0]))
        try:
            textrow = cur.fetchone()
            product.text = html2text(textrow[1].decode('utf-8'))
        except:
            pass

        thumbnail_path = row[9]
        _rel_dir = os.path.join('images', 'products', '{}_{}'.format(product.id, product.slug))
        _dir = os.path.join(BASE_DIR, 'static', _rel_dir)
        try:
            os.mkdir(_dir)
            shutil.copy(os.path.join(BASE_DIR, 'static', 'old', thumbnail_path), _dir)
        except OSError:
            pass
        product.thumbnail = os.path.join(_rel_dir, os.path.basename(thumbnail_path))

        # PRODUCT IMAGES
        cur.execute("""SELECT * from shop_itemforsaleimage WHERE item_id={}""".format(row[0]))
        for row in cur.fetchall():
            image_path = str(row[7])
            try:
                shutil.copy(os.path.join(BASE_DIR, 'static', 'old', image_path), _dir)
            except OSError:
                pass
            product_image = ProductImage(
                publish=True,
                order=row[3],
                product_id=product.id,
                path=os.path.join(_rel_dir, os.path.basename(image_path)),
                width=row[4],
                height=row[5],
            )
            db_session.add(product_image)
            db_session.flush()
            product_image.order = int(row[3])
            product_image.publish = True

        cur.execute("""SELECT * from shop_itemforsaleresource WHERE item_id={}""".format(old_id))
        # print(len(cur.fetchall()))
        for row in cur.fetchall():
            product_url = ProductUrl(
                publish=True,
                name=row[2].decode('utf-8'),
                order=int(row[6]),
                product_id=product.id,
                url=row[10].decode('utf-8'),
            )
            db_session.add(product_url)
            db_session.flush()
            product_url.order = int(row[6])
            product_url.publish = True

    db_session.commit()


def copy_members():
    cur.execute("""SELECT * from people_member""")
    for row in cur.fetchall():
        print('member:', row[2])
        member = Member(
            publish=True,
            first_name=row[1].decode('utf-8'),
            last_name=row[2].decode('utf-8'),
            bio=html2text(row[4]).decode('utf-8'),
            email=row[5].decode('utf-8'),
            city=row[6].decode('utf-8'),
            state=row[7].decode('utf-8'),
            headshot=None,
        )
        db_session.add(member)
        db_session.flush()

        headshot_path = row[8]
        _rel_dir = os.path.join('images', 'people', '{}_{}'.format(member.id, member.slug))
        _dir = os.path.join(BASE_DIR, 'static', _rel_dir)
        try:
            os.mkdir(_dir)
            shutil.copy(os.path.join(BASE_DIR, 'static', 'old', headshot_path), _dir)
        except OSError:
            pass
        member.headshot = os.path.join(_rel_dir, os.path.basename(headshot_path))

    db_session.commit()


def copy_collaborators():
    cur.execute("""SELECT * from people_collaborator""")
    for row in cur.fetchall():
        collaborator = Collaborator(
            publish=True,
            first_name=row[1].decode('utf-8'),
            last_name=row[2].decode('utf-8'),
            url=row[4].decode('utf-8'),
        )
        db_session.add(collaborator)
        db_session.flush()

        COLLABORATOR_ID_MAP[row[0]] = collaborator.id

        cur.execute("""SELECT * FROM people_collaborator_projects
            WHERE collaborator_id = {}""".format(row[0]))
        for row in cur.fetchall():
            collaborator.projects.append(
                db_session.query(Project).get(PROJECT_ID_MAP[row[2]])
            )
            db_session.flush()

    db_session.commit()


def add_search_vectors():
    engine.execute('ALTER TABLE project ADD COLUMN search_vector tsvector')
    engine.execute('ALTER TABLE product ADD COLUMN search_vector tsvector')
    engine.execute('ALTER TABLE member ADD COLUMN search_vector tsvector')
    engine.execute('CREATE INDEX project_search_index ON project USING gin(search_vector)')
    engine.execute('CREATE INDEX product_search_index ON product USING gin(search_vector)')
    engine.execute('CREATE INDEX member_search_index ON member USING gin(search_vector)')
    engine.execute('CREATE TRIGGER project_search_update BEFORE UPDATE OR INSERT ON project FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger("search_vector", "pg_catalog.english", "text", "long_name")')
    engine.execute('CREATE TRIGGER product_search_update BEFORE UPDATE OR INSERT ON product FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger("search_vector", "pg_catalog.english", "text", "long_name")')
    engine.execute('CREATE TRIGGER member_search_update BEFORE UPDATE OR INSERT ON member FOR EACH ROW EXECUTE PROCEDURE tsvector_update_trigger("search_vector", "pg_catalog.english", "bio")')


def add_search_view():

    # from sqlalchemy import DDL
    # search_view = DDL("""
    engine.execute("""DROP TABLE search;""")
    engine.execute("""
CREATE OR REPLACE VIEW search AS
  SELECT product.text AS text,
         product.long_name AS title,
         product.search_vector AS search_vector,
         'product' as object,
         product.id as object_id,
         product.id as id
    FROM product
  UNION ALL
  SELECT project.text AS text,
         project.long_name AS title,
         project.search_vector AS search_vector,
         'project' as object,
         project.id as object_id,
         project.id as id
    FROM project
  UNION ALL
  SELECT member.bio AS text,
         member.first_name || ' ' || member.last_name AS title,
         member.search_vector AS search_vector,
         'member' as object,
         member.id as object_id,
         member.id as id
    FROM member
;
    """)
    # conn = engine.connect()
    # conn.execute(search_view)
    # conn.close()
    # Base.metadata.reflect(bind=engine)
    # from obstructures.models import Search
    # Base.metadata.create_all(bind=engine)


def project_types_hack():
    slugs = {
        'hijacking-urban-decay': [6, ],
        'brutalist-habitat': [2, 3, ],
        'pallet-shelter': [1, ],
        'wall-less-mart': [2, 3, ],
        'snake-house': [2, 3, ],
        'osb-scape': [6, ],
        'rude-tectonics': [6, ],
        'no-minarets': [2, 3, ],
        'tacticalworks-hq': [1, 4, ],
        'drawer-house': [2, 3, ],
        'a-light-occupation': [6, ],
        'waste-is-a-thief': [2, ],
        'nc-aia-hq': [2, 3, ],
        'flower-pot-florist': [1, 4, ],
        'vapid-rigor': [],
        'disassembly-line': [6, ],
        'abc-aluminum-guitar': [8, 9, ],
        'wallet-aluminum-plate': [7, 11, ],
        '0-625-brut-guitar': [8, 9, ],
        '0-750-guitar-two-tone': [8, 9, ],
        '0-750-guitar-clear': [8, 9, ],
        '0-750-bass-guitar': [8, 9, ],
        'aluminum-drums': [8, 9, ],
        'channel-lamp': [8, 16, ],
        'stud-lamp': [8, 16, ],
        'tool-pry-open-v1': [8, 10, ],
        'notes-of-valor': [12, ],
        'brut-unison': [18, ],
        'octavo': [12, ],
        '3ct-web': [15, ],
        'ardbeg': [14, ],
        'lettering': [14, ],
        'amta-textbook': [12, ],
        'axon-calc': [17, ],
        'climate-emulator': [17, ],
        'ut-coad-wall': [1, 4, ],
        'house-with-two-courts': [1, 3, ],
        'slash-graphic': [13, ],
        'tool-pry-open': [7, 10, ],
        '0-750b-aluminum-guitar': [7, 9, ],
        'long-live-the-landsarkivet': [], 
        'mailbox': [8, ],
        'display-panel-system': [8, ],
        'bandboard-work-platform': [7, 11, ],
        'linescape': [1, 5, ],
        'a-cynical-manifesto': [20, ],
        'grid-isometric-paper': [7, ],
        'villa-brut-knives-split-7': [18, ],
        'fifa-2018': [19, ],
    }
    for slug in slugs:
        print slug
        project = Project.query.filter(Project.slug == slug).one()
        project_types = []
        for project_type_id in slugs[slug]:
            project_types.append(ProjectType.query.get(project_type_id))
        project.project_types = project_types
        db_session.commit()


if __name__ == '__main__':
    # pass
    init_db()
    ## add_search_vectors()
    copy_projects()
    copy_itemsforsale()
    copy_members()
    copy_collaborators()
    #
    add_search_view()
    project_types_hack()