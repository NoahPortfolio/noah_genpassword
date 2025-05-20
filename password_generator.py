import string
from random import choice
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

BG_COLOR = "#2d3748"
SECONDARY_COLOR = "#4a5568"
ACCENT_COLOR = "#4299e1"
TEXT_COLOR = "#f7fafc"
ENTRY_COLOR = "#1a202c"
HOVER_COLOR = "#3182ce"

def generate_password():
    try:
        length = int(length_var.get())
        include_special_chars = special_chars_var.get()
        include_numbers = numbers_var.get()
        include_uppercase = uppercase_var.get()

        all_chars = string.ascii_lowercase
        if include_uppercase:
            all_chars += string.ascii_uppercase
        if include_numbers:
            all_chars += string.digits
        if include_special_chars:
            all_chars += string.punctuation

        if not all_chars:
            messagebox.showwarning("Attention", "Veuillez sélectionner au moins un type de caractères")
            return

        password = "".join(choice(all_chars) for _ in range(length))
        
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        password_entry.config(fg=ACCENT_COLOR)

        app_name = app_name_entry.get().strip()
        if app_name:
            try:
                with open("mesmotdepasse.txt", "a+", encoding='utf-8') as file:
                    file.write(f"{app_name} : {password}\n")
                status_label.config(text="Mot de passe enregistré!", fg="#48bb78")
            except IOError:
                status_label.config(text="Erreur d'enregistrement", fg="#e53e3e")
        else:
            status_label.config(text="Entrez un nom d'application", fg="#e53e3e")
            
        generate_button.config(text="✓ Généré!")
        window.after(1500, lambda: generate_button.config(text="Générer mot de passe"))
        
    except ValueError:
        messagebox.showerror("Erreur", "La longueur doit être un nombre valide")

def copy_to_clipboard():
    window.clipboard_clear()
    window.clipboard_append(password_entry.get())
    status_label.config(text="Copié dans le presse-papier!", fg="#48bb78")
    window.after(2000, lambda: status_label.config(text="", fg=TEXT_COLOR))

def toggle_advanced():
    if advanced_frame.winfo_ismapped():
        advanced_frame.grid_remove()
        toggle_button.config(text="Options avancées ▼")
    else:
        advanced_frame.grid()
        toggle_button.config(text="Options avancées ▲")

def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter?"):
        window.destroy()

window = tk.Tk()
window.title("Gen Password")
window.geometry("800x600")
window.resizable(False, False)
window.configure(bg=BG_COLOR)
window.protocol("WM_DELETE_WINDOW", on_closing)

style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=BG_COLOR)
style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR)
style.configure('TButton', background=ACCENT_COLOR, foreground=TEXT_COLOR, 
                font=('Helvetica', 12, 'bold'), borderwidth=0)
style.map('TButton', background=[('active', HOVER_COLOR), ('pressed', HOVER_COLOR)])

header_frame = ttk.Frame(window, style='TFrame')
header_frame.pack(pady=(20, 10))

title_label = ttk.Label(header_frame, text="Gen Password", font=('Helvetica', 28, 'bold'), 
                       foreground=ACCENT_COLOR, background=BG_COLOR)
title_label.pack()

subtitle_label = ttk.Label(header_frame, text="Générateur de mots de passe sécurisés", 
                          font=('Helvetica', 12), foreground=TEXT_COLOR)
subtitle_label.pack(pady=(5, 0))

main_frame = ttk.Frame(window, style='TFrame')
main_frame.pack(pady=20, padx=40, fill='both', expand=True)

app_name_label = ttk.Label(main_frame, text="Pour quel service?", font=('Helvetica', 12))
app_name_label.grid(row=0, column=0, sticky='w', pady=(0, 5))

app_name_entry = ttk.Entry(main_frame, font=('Helvetica', 12), width=30)
app_name_entry.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky='ew')

length_label = ttk.Label(main_frame, text="Longueur du mot de passe", font=('Helvetica', 12))
length_label.grid(row=2, column=0, sticky='w', pady=(10, 5))

length_var = tk.StringVar(value="16")
length_scale = ttk.Scale(main_frame, from_=8, to=32, variable=length_var, 
                        command=lambda v: length_value.config(text=f"{int(float(v))}"))
length_scale.grid(row=3, column=0, sticky='ew', pady=(0, 5))

length_value = ttk.Label(main_frame, text="16", font=('Helvetica', 12), width=3)
length_value.grid(row=3, column=1, sticky='w', padx=(10, 0))

toggle_button = ttk.Button(main_frame, text="Options avancées ▼", 
                          command=toggle_advanced, style='TButton')
toggle_button.grid(row=4, column=0, pady=(20, 5), sticky='w')

advanced_frame = ttk.Frame(main_frame, style='TFrame')

special_chars_var = tk.BooleanVar(value=True)
special_chars_check = ttk.Checkbutton(advanced_frame, text="Caractères spéciaux (!@#...)", 
                                    variable=special_chars_var)
special_chars_check.grid(row=0, column=0, sticky='w', pady=2)

numbers_var = tk.BooleanVar(value=True)
numbers_check = ttk.Checkbutton(advanced_frame, text="Chiffres (0-9)", 
                               variable=numbers_var)
numbers_check.grid(row=1, column=0, sticky='w', pady=2)

uppercase_var = tk.BooleanVar(value=True)
uppercase_check = ttk.Checkbutton(advanced_frame, text="Lettres majuscules (A-Z)", 
                                variable=uppercase_var)
uppercase_check.grid(row=2, column=0, sticky='w', pady=2)

advanced_frame.grid(row=5, column=0, columnspan=2, pady=(0, 20), sticky='ew')
advanced_frame.grid_remove()

password_label = ttk.Label(main_frame, text="Mot de passe généré", font=('Helvetica', 12))
password_label.grid(row=6, column=0, sticky='w', pady=(10, 5))

password_frame = ttk.Frame(main_frame, style='TFrame')
password_frame.grid(row=7, column=0, columnspan=2, sticky='ew')

password_entry = ttk.Entry(password_frame, font=('Helvetica', 14), width=25)
password_entry.pack(side='left', fill='x', expand=True, ipady=8)

copy_button = ttk.Button(password_frame, text="📋", width=3, command=copy_to_clipboard)
copy_button.pack(side='right', padx=(5, 0))

generate_button = ttk.Button(main_frame, text="Générer mot de passe", 
                           command=generate_password, style='TButton')
generate_button.grid(row=8, column=0, columnspan=2, pady=(20, 5), sticky='ew')

status_label = tk.Label(main_frame, text="", font=('Helvetica', 10), bg=BG_COLOR, fg=TEXT_COLOR)
status_label.grid(row=9, column=0, columnspan=2, pady=(5, 0))

footer_frame = ttk.Frame(window, style='TFrame')
footer_frame.pack(side='bottom', pady=(0, 20))

footer_label = ttk.Label(footer_frame, text="© 2025 Gen Password - Tous droits réservés", 
                        font=('Helvetica', 9), foreground=SECONDARY_COLOR)
footer_label.pack()

window.mainloop()