import os


def get_secret_value(key):
    """
    With the given key, this function will return the secret value, created with docker secrets.
    """
    base_dir = os.path.relpath("../../run/secrets/", start=os.curdir)
    file_name = key
    file_path = os.path.join(base_dir, file_name)

    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            secret_value_file = f.read().splitlines()
            secret_value = secret_value_file[0].strip(' "')
            return secret_value

    return print("This secret does not exist.")
