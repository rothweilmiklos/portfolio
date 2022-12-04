import jwt


PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoJVchiFeb5bpOsHQ+ZR8Ho3dCAc7x+4+GxeId/Hj+OwoLRb8nqt/DxE9XkuN04o1LYeflPVskjmxjO3mwKSUdjx0C05TOg9U2c+v7l1AGnYlYQxZtOn2axx9AdzEyJoky3pp4dS5GBbrjGwxHu+83LOPDWmeONRZJeBhk0tclW19t/kqBPH+JilwCWog/lZgDPRH8oXaiXOJ9VdE0xRh3Yi6Fi18JnB5nHAEQT+aVFSNM05/CleOQ2x8P0PKEW//pVemgeOAthCRxDgM0YXKJ0xBiKi3wtYEGrPBwQulGxepxCcOr0vrAaCKYAehFca8F+IPx7ytuCeq+fHocq9WVwIDAQAB\n-----END PUBLIC KEY-----'


def decode_access_token(access_token):
    decoded_token = jwt.decode(access_token, PUBLIC_KEY, algorithms=["RS256"],
                               options={"verify_signature": False})

    return decoded_token
