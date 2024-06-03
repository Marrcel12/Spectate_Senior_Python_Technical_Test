import re
from distutils.util import strtobool


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\s-]", "", value).strip().lower()
    value = re.sub(r"[-\s]+", "-", value)
    return value


def bool_string_to_int(value):
    """
    Converts a string representation of a boolean to 1 or 0.

    Parameters:
        value (str): The input string value.

    Returns:
        int or str: Returns 1 for "True", 0 for "False", and the original string if it's not a boolean string.
    """
    try:
        return strtobool(value)
    except ValueError:
        return value
