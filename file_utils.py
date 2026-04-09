# file_utils.py

def save_to_file(filename, data):
    with open(filename, 'w') as f:
        f.write(','.join(map(str, data)))


def load_from_file(filename):
    with open(filename, 'r') as f:
        return list(map(int, f.read().split(',')))