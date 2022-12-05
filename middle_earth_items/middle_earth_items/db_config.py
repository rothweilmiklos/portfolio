import os
from . import secret_key


def dev_or_prod_db(debug, base_directory):
    if debug == 1:
        SQLITE_DATABASE = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_directory / 'db.sqlite3',
        }
        return SQLITE_DATABASE
    else:
        #for development uncomment the three lines below and comment the three lines below that
        # POSTGRES_DB = os.environ.get('POSTGRES_DB')
        # POSTGRES_USER = os.environ.get('POSTGRES_USER')
        # POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

        # for production uncomment the three lines below, and comment the three lines above
        POSTGRES_DB = secret_key.get_secret_value('items_postgres_db')
        POSTGRES_USER = secret_key.get_secret_value('items_postgres_user')
        POSTGRES_PASSWORD = secret_key.get_secret_value('items_postgres_password')

        POSTGRESQL_DATABASE = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'db_items',
            'PORT': '5432',
        }
        return POSTGRESQL_DATABASE
