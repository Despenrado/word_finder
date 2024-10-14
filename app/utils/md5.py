import hashlib


def calculate_md5_from_data_and_pattern(_, data, pattern):
    if pattern is None:
        pattern = ""
    if data is None:
        data = b""

    data = pattern.encode('utf-8') + data
    return hashlib.md5(data).hexdigest()
