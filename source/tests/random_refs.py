import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_bookmark(name=""):
    return f"bookmark-{name}-{random_suffix()}"


