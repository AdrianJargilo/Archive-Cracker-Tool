import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import zipfile
import rarfile
import py7zr
import itertools

def try_password(file_path, password):
    # Tries to open the archive with the given password.
    # Returns True if the password is correct, False otherwise.
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
    except Exception:
        return False

def crack_archive(archive_file_path, dictionary_file_path, stop_event):
    def run_dictionary_attack():
        # Dictionary attack: tries each password from the dictionary file.
        try:
            with open(dictionary_file_path, 'r') as dict_file:
                for line in dict_file:
                    if stop_event.is_set():
                        update_password_display("Search stopped.")
                        return
                    password = line.strip()
                    update_password_display(f"Trying: {password}")
                    if try_password(archive_file_path, password):
                        update_password_display(f"Password found: {password}")
                        return
            if not stop_event.is_set():
                # If password is not found in dictionary, ask user to start brute-force attack.
                response = messagebox.askyesno("Password Not Found", "Password not found in dictionary. Do you want to start a brute-force attack?")
                if response:
                    run_brute_force_attack()
                else:
                    update_password_display("Password not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            update_password_display("Error")

    def run_brute_force_attack():
        # Brute-force attack: tries combinations of characters up to a certain length.
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        for length in range(1, 6):  # Limit of password length for brute-force
            for password in itertools.product(alphabet, repeat=length):
                if stop_event.is_set():
                    update_password_display("Brute-force stopped.")
                    return
                password = ''.join(password)
                update_password_display(f"Trying: {password}")
                if try_password(archive_file_path, password):
                    update_password_display(f"Password found: {password}")
                    return
        if not stop_event.is_set():
            update_password_display("Password not found in brute-force attack.")

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

def start_attack():
    # Starts or stops the attack based on the current state of the start button.
    global attack_thread, stop_event
    if start_button["text"] == "Start Attack":
        stop_event.clear()
        attack_thread = crack_archive(archive_entry.get(), dict_entry.get(), stop_event)
        start_button.config(text="Stop", bg="#f44336")
    else:
        stop_event.set() # Signals the attack thread to stop
        start_button.config(text="Start Attack", bg="#4CAF50")
        password_label.config(text="Stopping...")

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

stop_event = threading.Event()
attack_thread = None
start_button = tk.Button(root, text="Start Attack", command=start_attack, bg='#4CAF50', fg='white')
start_button.grid(row=3, column=1, padx=10, pady=10)

password_label = tk.Label(root, text="", **style)
password_label.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
