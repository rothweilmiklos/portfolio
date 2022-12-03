from . import secret_key


def dev_or_prod_db(debug, base_directory):
    if debug == 1:
        SQLITE_DATABASE = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_directory / 'db.sqlite3',
        }
        return SQLITE_DATABASE
    else:
        POSTGRES_DB = secret_key.get_secret_value('postgres_db')
        POSTGRES_USER = secret_key.get_secret_value('postgres_user')
        POSTGRES_PASSWORD = secret_key.get_secret_value('postgres_password')

        POSTGRESQL_DATABASE = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': POSTGRES_DB,
            'USER': POSTGRES_USER,
            'PASSWORD': POSTGRES_PASSWORD,
            'HOST': 'portfolio_db',
            # Host is called portfolio_db, because the container declared in docker-compose.yaml is called portfolio_db
            'PORT': '5432',
            'CONN_MAX_AGE': None,
        }
        return POSTGRESQL_DATABASE
