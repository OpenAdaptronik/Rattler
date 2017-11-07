import os
from migrate.versioning import api
from migrate.exceptions import DatabaseAlreadyControlledError
from app import db
from app.tasks import command
from config import SQLALCHEMY_MIGRATE_REPO, SQLALCHEMY_DATABASE_URI


@command
def init_db():
    db.create_all()
    try:
        if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
            api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
        else:
            api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
    except DatabaseAlreadyControlledError:
        print('Database allready initilized')