import jwt
from . import constants

PUBLIC_KEY = constants.PUBLIC_KEY


def decode_access_token(access_token):
    decoded_token = jwt.decode(access_token, PUBLIC_KEY, algorithms=["RS256"],
                               options={"verify_signature": False})

    return decoded_token
