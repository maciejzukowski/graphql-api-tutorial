import os
import logging

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from contextlib import contextmanager


def log_queries():
    import time
    from sqlalchemy import event
    from sqlalchemy.engine import Engine
    logging.basicConfig()
    logger = logging.getLogger("myapp.sqltime")
    logger.setLevel(logging.DEBUG)

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement,
                            parameters, context, executemany):
        conn.info.setdefault('query_start_time', []).append(time.time())

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement,
                            parameters, context, executemany):
        total = time.time() - conn.info['query_start_time'].pop(-1)
        logger.debug(str(cursor.query).replace('\\n',' '))
        logger.debug("Total Time: %f" % total)

if os.environ.get('DBV'):
    log_queries()


def postgresql_connect_url():
    return os.environ.get("DATABASE_URL") if os.environ.get("DATABASE_URL") else os.environ.get("TEST_DATABASE_URL")


engine = sa.create_engine(postgresql_connect_url(), convert_unicode=True,connect_args={
            'application_name': os.environ.get('DYNO','MyApp'),
        })
db_session = sa_orm.scoped_session(sa_orm.sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class _Globals:
    session_factory = None
    engine = None



def get_engine():
    if not _Globals.engine:
        connect_url = postgresql_connect_url()
        _Globals.engine = sa.create_engine(connect_url, connect_args={
            'application_name': os.environ.get('DYNO','MyApp'),
        })

    return _Globals.engine


def get_factory():
    if not _Globals.session_factory:
        dbengine = get_engine()
        _Globals.session_factory = sa_orm.sessionmaker(
            bind=dbengine, autocommit=False, autoflush=False, expire_on_commit=True)

    return _Globals.session_factory


def get_connection():
    return get_engine().connect()

@contextmanager
def session():
    session_factory = get_factory()
    session = sa_orm.scoped_session(session_factory)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()