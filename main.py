import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import rarfile
import py7zr
import threading
import itertools

def crack_archive(archive_file_path, dictionary_file_path):
    def run_dictionary_attack():
        try:
            with open(dictionary_file_path, 'r') as dict_file:
                for line in dict_file:
                    password = line.strip()
                    update_password_display(f"Trying: {password}")
                    if try_password(archive_file_path, password):
                        update_password_display(f"Password found: {password}")
                        return
            response = messagebox.askyesno("Password Not Found", "Password not found in dictionary. Do you want to start a brute-force attack?")
            if response:
                run_brute_force_attack()
            else:
                update_password_display("Password not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            update_password_display("Error")

    def run_brute_force_attack():
        alphabet = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890"
        for length in range(1, 6):
            for password in itertools.product(alphabet, repeat=length):
                password = ''.join(password)
                update_password_display(f"Trying: {password}")
                if try_password(archive_file_path, password):
                    update_password_display(f"Password found: {password}")
                    return
        update_password_display("Password not found.")

    def try_password(file_path, password):
        try:
            if file_path.endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as archive:
                    archive.extractall(pwd=bytes(password, 'utf-8'))
            elif file_path.endswith('.rar'):
                with rarfile.RarFile(file_path, 'r') as archive:
                    archive.extractall(pwd=password)
            elif file_path.endswith('.7z'):
                with py7zr.SevenZipFile(file_path, 'r', password=password) as archive:
                    archive.extractall()
            return True
        except (zipfile.BadZipFile, rarfile.BadRarFile, py7zr.Bad7zFile):
            return False
        except Exception as e:
            return False

    attack_thread = threading.Thread(target=run_dictionary_attack)
    attack_thread.start()

def select_archive():
    path = filedialog.askopenfilename()
    archive_entry.delete(0, tk.END)
    archive_entry.insert(0, path)

def select_dict():
    path = filedialog.askopenfilename()
    dict_entry.delete(0, tk.END)
    dict_entry.insert(0, path)

def update_password_display(password):
    password_label.config(text=password)

root = tk.Tk()
root.title("Archive Cracker")
root.configure(bg='#f0f0f0')
root.iconbitmap('icon.ico')

style = {'font': ('Helvetica', 12), 'bg': '#f0f0f0'}

tk.Label(root, text="Archive File:", **style).grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, text="Dictionary File:", **style).grid(row=2, column=0, padx=10, pady=10)

archive_entry = tk.Entry(root, width=50)
dict_entry = tk.Entry(root, width=50)

archive_entry.grid(row=1, column=1, padx=10, pady=10)
dict_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Browse", command=select_archive).grid(row=1, column=2, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_dict).grid(row=2, column=2, padx=10, pady=10)
tk.Button(root, text="Start Attack", command=lambda: crack_archive(archive_entry.get(), dict_entry.get()), bg='#4CAF50', fg='white').grid(row=3, column=1, padx=10, pady=10)

password_label = tk.Label(root, text="", **style)
password_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
