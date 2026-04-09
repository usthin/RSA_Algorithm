# main.py

import tkinter as tk
from rsa_core import generate_keys, encrypt, decrypt, factor_n, mod_inverse
from file_utils import save_to_file, load_from_file

# ------------------ ENCRYPT ------------------
def run_encryption():
    try:
        p = int(entry_p.get())
        q = int(entry_q.get())
        text = entry_text.get()

        public, private, phi = generate_keys(p, q)

        encrypted = encrypt(text, public)

        save_to_file("encrypted.txt", encrypted)

        result_label.config(
            text=f"Encrypted: {encrypted}\nPublic key: {public}"
        )

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


# ------------------ DECRYPT ------------------
def run_decryption():
    try:
        n = int(entry_n.get())
        e = int(entry_e.get())

        cipher = load_from_file("encrypted.txt")

        # factor n → find p and q
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
root.geometry("400x500")

# Inputs for encryption
tk.Label(root, text="Prime p").pack()
entry_p = tk.Entry(root)
entry_p.pack()

tk.Label(root, text="Prime q").pack()
entry_q = tk.Entry(root)
entry_q.pack()

tk.Label(root, text="Text to encrypt").pack()
entry_text = tk.Entry(root)
entry_text.pack()

tk.Button(root, text="Encrypt", command=run_encryption).pack(pady=10)

# Inputs for decryption
tk.Label(root, text="n (public)").pack()
entry_n = tk.Entry(root)
entry_n.pack()

tk.Label(root, text="e (public)").pack()
entry_e = tk.Entry(root)
entry_e.pack()

tk.Button(root, text="Decrypt", command=run_decryption).pack(pady=10)

# Output
result_label = tk.Label(root, text="", wraplength=350, justify="left")
result_label.pack(pady=20)

root.mainloop()