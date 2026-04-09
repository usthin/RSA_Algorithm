# file_utils.py

def save_full_data(filename, encrypted_data, public_key):
    n, e = public_key

    with open(filename, 'w') as f:
        f.write(f"n={n}\n")
        f.write(f"e={e}\n")
        f.write("cipher=" + ','.join(map(str, encrypted_data)))


def load_full_data(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    n = int(lines[0].split('=')[1].strip())
    e = int(lines[1].split('=')[1].strip())
    cipher = list(map(int, lines[2].split('=')[1].split(',')))

    return (n, e), cipher