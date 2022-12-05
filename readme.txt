If production mode is wanted, the code parts below needs to be changed:
    - project:portfolio:
        - in settings.py debug and secret_key values needs to be commented/uncommented as stated in that file
        - in settings.py aws_access_key and aws_secret_key values needs to be commented/uncommented as stated in that file

    - project: middle_earth_front:
        - in decode.py public_key needs to be commented/uncommented
        - in settings.py debug and secret_key needs to commented/uncommented
        - in db_config postgres_user, postgres_password, postgres_db needs to commented/uncommented

    - project: middle_earth_auth:
        - in settings.py signing_key, public_key needs to be commented/uncommented
        - in settings.py debug and secret_key needs to commented/uncommented
        - in db_config postgres_user, postgres_password, postgres_db needs to commented/uncommented

    - project: middle_earth_items:
        - in settings.py debug and secret_key needs to commented/uncommented
        - in db_config postgres_user, postgres_password, postgres_db needs to commented/uncommented

    - project: middle_earth_invetory:
        - in settings.py signing_key, public_key needs to be commented/uncommented
        - in settings.py debug and secret_key needs to commented/uncommented
        - in db_config postgres_user, postgres_password, postgres_db needs to commented/uncommented

    - docker_compose.yaml
        - environmental/secrets comment/uncomment
        - build/image comment/uncomment