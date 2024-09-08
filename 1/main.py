import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import os
import platform

# Функция для открытия файла и отображения изображения
def open_image():
    filetypes = [
        ("Image Files", "*.bmp;*.jpg;*.jpeg;*.gif;*.png"),
        ("All files", "*.*")
    ]
    filepath = filedialog.askopenfilename(title="Открыть изображение", filetypes=filetypes)
    
    if filepath:
        try:
            img = Image.open(filepath)
            img = img.resize((picture_box.winfo_width(), picture_box.winfo_height()), Image.Resampling.LANCZOS)  # Заменили ANTIALIAS на LANCZOS
            img_tk = ImageTk.PhotoImage(img)
            picture_box.config(image=img_tk)
            picture_box.image = img_tk  # Для предотвращения сборки мусора
        except UnidentifiedImageError:
            messagebox.showerror("Ошибка", "Некорректный формат изображения. Пожалуйста, выберите правильный файл изображения (.png, .jpeg, .bmp, .gif)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при открытии изображения: {str(e)}")
    
# Функция для отображения информации о системе
def show_system_info():
    info = f"""
    Имя компьютера: {platform.node()}
    Операционная система: {platform.system()} {platform.release()} ({platform.version()})
    Архитектура: {platform.machine()}
    Процессор: {platform.processor()}
    Платформа: {platform.platform()}
    Путь к домашнему каталогу: {os.path.expanduser('~')}
    """
    messagebox.showinfo("Информация о системе", info)

# Создаем основное окно
root = tk.Tk()
root.title("Просмотреть изображение")
root.geometry("800x800")

# Создаем компонент для отображения изображения
picture_box = tk.Label(root, text="Здесь будет изображение")
picture_box.pack(expand=True, fill=tk.BOTH)

# Создаем кнопку для открытия изображения
open_button = tk.Button(root, text="Открыть изображение", command=open_image)
open_button.pack(side=tk.RIGHT, anchor="se", padx=10, pady=10)

# Создаем меню для отображения информации о системе
menubar = tk.Menu(root)
system_menu = tk.Menu(menubar, tearoff=0)
system_menu.add_command(label="Информация о системе", command=show_system_info)
menubar.add_cascade(label="Система", menu=system_menu)
root.config(menu=menubar)

# Запускаем основной цикл приложения
root.mainloop()
