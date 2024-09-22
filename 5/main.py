import tkinter as tk
from tkinter import Listbox, END, filedialog
import os

# Функция для отображения содержимого выбранной директории
def show_directory():
    selected_item = file_listbox.get(tk.ACTIVE)
    
    if selected_item.startswith("[DIR]"):
        # Получаем название папки без префикса "[DIR] "
        folder_name = selected_item[6:]
        new_path = os.path.join(current_path.get(), folder_name)
        if os.path.isdir(new_path):
            current_path.set(new_path)
            update_file_list(new_path)

# Функция для перехода в предыдущую директорию
def go_back():
    parent_directory = os.path.dirname(current_path.get())
    current_path.set(parent_directory)
    update_file_list(parent_directory)

# Функция для обновления содержимого ListBox с файлами
def update_file_list(path):
    file_listbox.delete(0, END)
    file_listbox.insert(END, "..")  # Для перехода назад
    try:
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                display_text = f"[DIR] {item}"
                file_listbox.insert(END, display_text)
            else:
                ext = os.path.splitext(item)[1].lower()  # Получаем расширение
                display_text = f"{item}"
                
                # Подсветка в зависимости от расширения
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

# Функция для выбора директории через стандартное диалоговое окно Windows
def choose_directory():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        current_path.set(selected_dir)
        update_file_list(selected_dir)

# Создаем интерфейс приложения
root = tk.Tk()
root.title("Файловая структура диска")
root.geometry("600x500")

# Строка для текущего пути
current_path = tk.StringVar()
current_path.set("/")

# Label для отображения текущего пути
path_label = tk.Label(root, textvariable=current_path)
path_label.pack(pady=10)

# ListBox для отображения содержимого папок
file_listbox = Listbox(root, width=80, height=20)
file_listbox.pack(pady=10)

# Кнопки для отображения, возврата к предыдущему каталогу и выбора папки
show_button = tk.Button(root, text="Отобразить", command=show_directory)
show_button.pack(side="left", padx=20)

back_button = tk.Button(root, text="Назад", command=go_back)
back_button.pack(side="left")

choose_button = tk.Button(root, text="Выбрать папку", command=choose_directory)
choose_button.pack(side="left", padx=20)

# Инициализация отображения корневого каталога
update_file_list(current_path.get())

# Запуск основного цикла окна
root.mainloop()
