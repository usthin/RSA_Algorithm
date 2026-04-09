# main.py

import tkinter as tk
from rsa_core import generate_keys, encrypt, decrypt, factor_n, mod_inverse
from file_utils import save_full_data, load_full_data

FILENAME = "encrypted.txt"


# ------------------ ENCRYPT ------------------
def run_encryption():
    try:
        p = int(entry_p.get())
        q = int(entry_q.get())
        text = entry_text.get()

        public, private, phi = generate_keys(p, q)
        encrypted = encrypt(text, public)

        save_full_data(FILENAME, encrypted, public)

        result_label.config(
            text=f"Encrypted saved to {FILENAME}\nPublic key: {public}"
        )

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


# ------------------ LOAD FROM FILE ------------------
def load_data():
    try:
        public, cipher = load_full_data(FILENAME)

        n, e = public

        entry_n.delete(0, tk.END)
        entry_n.insert(0, str(n))

        entry_e.delete(0, tk.END)
        entry_e.insert(0, str(e))

        result_label.config(text=f"Loaded from file:\nCipher: {cipher}")

    except Exception as e:
        result_label.config(text=f"Error loading file: {str(e)}")


# ------------------ DECRYPT ------------------
def run_decryption():
    try:
        n = int(entry_n.get())
        e = int(entry_e.get())

        public, cipher = load_full_data(FILENAME)

        p, q = factor_n(n)

        if not p:
            result_label.config(text="Failed to factor n")
            return

        phi = (p - 1) * (q - 1)
        d = mod_inverse(e, phi)

        decrypted = decrypt(cipher, (n, d))

        result_label.config(
            text=f"Decrypted: {decrypted}\np={p}, q={q}, d={d}"
        )

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


# ------------------ UI ------------------
root = tk.Tk()
root.title("RSA Encryption System")
root.geometry("420x550")

# Encryption inputs
tk.Label(root, text="Prime p").pack()
entry_p = tk.Entry(root)
entry_p.pack()

tk.Label(root, text="Prime q").pack()
entry_q = tk.Entry(root)
entry_q.pack()

tk.Label(root, text="Text to encrypt").pack()
entry_text = tk.Entry(root)
entry_text.pack()

tk.Button(root, text="Encrypt & Save", command=run_encryption).pack(pady=10)

# Load button
tk.Button(root, text="Load from File", command=load_data).pack(pady=5)

# Decryption inputs
tk.Label(root, text="n (public)").pack()
entry_n = tk.Entry(root)
entry_n.pack()

tk.Label(root, text="e (public)").pack()
entry_e = tk.Entry(root)
entry_e.pack()

tk.Button(root, text="Decrypt", command=run_decryption).pack(pady=10)

# Output
result_label = tk.Label(root, text="", wraplength=380, justify="left")
result_label.pack(pady=20)

root.mainloop()