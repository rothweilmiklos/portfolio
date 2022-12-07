import os
from . import secret_key


def dev_or_prod_db(debug, base_directory):
    if debug:
        SQLITE_DATABASE = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_directory / 'db.sqlite3',
        }
        return SQLITE_DATABASE
    else:
        #for development uncomment the three lines below and comment the three lines below that
        # POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

        # for production uncomment the three lines below, and comment the three lines above
        POSTGRES_PASSWORD = secret_key.get_secret_value('items_postgres_password')

        POSTGRESQL_DATABASE = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'db_items',
            'PORT': '5432',
        }
        return POSTGRESQL_DATABASE
