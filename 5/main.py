import tkinter as tk
from tkinter import Listbox, END, filedialog
import os

def show_directory():
    selected_item = file_listbox.get(tk.ACTIVE)
    
    if selected_item.startswith("[DIR]"):
        folder_name = selected_item[6:]
        new_path = os.path.join(current_path.get(), folder_name)
        if os.path.isdir(new_path):
            current_path.set(new_path)
            update_file_list(new_path)

def go_back():
    parent_directory = os.path.dirname(current_path.get())
    current_path.set(parent_directory)
    update_file_list(parent_directory)

def update_file_list(path):
    file_listbox.delete(0, END)
    try:
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                display_text = f"[DIR] {item}"
                file_listbox.insert(END, display_text)
            else:
                ext = os.path.splitext(item)[1].lower()
                display_text = f"{item}"
                
                if ext == ".txt":
                    file_listbox.insert(END, display_text)
                    file_listbox.itemconfig(END, {'fg': 'blue'})
                elif ext in [".jpg", ".png", ".gif"]:
                    file_listbox.insert(END, display_text)
                    file_listbox.itemconfig(END, {'fg': 'green'})
                elif ext in [".exe", ".bat"]:
                    file_listbox.insert(END, display_text)
                    file_listbox.itemconfig(END, {'fg': 'red'})
                else:
                    file_listbox.insert(END, display_text)
    except Exception as e:
        pass

def choose_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        current_path.set(selected_dir)
        update_file_list(selected_dir)

root = tk.Tk()
root.title("Файловая структура диска")
root.geometry("600x500")

current_path = tk.StringVar()
current_path.set("/")

path_label = tk.Label(root, textvariable=current_path)
path_label.pack(pady=10)

file_listbox = Listbox(root, width=80, height=20)
file_listbox.pack(pady=10)

show_button = tk.Button(root, text="Отобразить", command=show_directory)
show_button.pack(side="left", padx=20)

back_button = tk.Button(root, text="Назад", command=go_back)
back_button.pack(side="left")

choose_button = tk.Button(root, text="Выбрать папку", command=choose_directory)
choose_button.pack(side="left", padx=20)

update_file_list(current_path.get())

root.mainloop()
