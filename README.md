# Archive Cracker Tool

## Description

This Archive Cracker Tool is a Python-based graphical user interface application that performs dictionary attacks on ZIP, RAR, and 7z files. It's designed for educational purposes to demonstrate how a basic dictionary attack works. The user can select an archive file and a dictionary file (a text file with potential passwords) through the interface. The tool will attempt to find the correct password for the file and also supports a brute-force attack if the password is not found in the dictionary.

## Setup

### Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)
- Pillow Library: Install it via pip with `pip install pillow`
- Additional libraries: `rarfile`, `py7zr`. Install them via pip with `pip install rarfile py7zr`

### Installation

1. Clone or download this repository to your local machine.
2. Ensure Python 3.x is installed on your system.
3. Install Pillow, rarfile, and py7zr using pip if they're not already installed.

### Files

- `archive_cracker.py`: Main Python script for the Archive Cracker Tool.
- `icon.ico`: Icon file for the application (ensure this is in the same directory as `archive_cracker.py`).

## Usage

1. Run `archive_cracker.py`.
2. Use the "Browse" buttons to select the archive file you want to crack and the dictionary file (a plain text file with one password per line).
3. Click "Start Attack" to begin the dictionary attack.
4. If the password is not found in the dictionary, you will be prompted to start a brute-force attack.
5. The tool will display the found password or a message if the password is not found. You can stop the attack at any time by clicking "Stop".

## Disclaimer

This tool is for educational purposes only. Unauthorized cracking of archive files is illegal and unethical. Use this tool only for legitimate educational purposes, such as learning about cybersecurity methods or performing penetration testing with permission.
