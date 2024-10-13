import hashlib


def calculate_md5_from_data_and_pattern(_, data, pattern):
    data = pattern.encode('utf-8') + data
    return hashlib.md5(data).hexdigest()


def calculate_md5_from_table_and_pattern(_, headers, rows, pattern):
    data = pattern + ''.join(map(str, headers)) + ''.join([''.join(map(str, row)) for row in rows])
    hashed = hashlib.md5(data.encode()).hexdigest()
    return hashed