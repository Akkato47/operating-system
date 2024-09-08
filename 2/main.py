import tkinter as tk
from tkinter import filedialog, messagebox

# Глобальные переменные
sort_method = "length"  # Текущий метод сортировки: "length" или "alphabetical"
sort_order = "ascending"  # Текущий порядок сортировки: "ascending" или "descending"

# Функция для выбора и открытия файла с учетом кодировки
def open_file():
    filetypes = [
        ("Text Files", "*.txt"),
        ("All files", "*.*")
    ]
    filepath = filedialog.askopenfilename(title="Открыть файл", filetypes=filetypes)
    
    if filepath:
        encodings = ['utf-8', 'windows-1251', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                    listbox.delete(0, tk.END)  # Очистить Listbox перед добавлением новых элементов
                    for line in lines:
                        listbox.insert(tk.END, line.strip())  # Вставляем каждую строку в Listbox
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл: {str(e)}")
                break

# Функция для удаления пустых строк из Listbox
def remove_empty_lines():
    items = listbox.get(0, tk.END)
    non_empty_items = [item for item in items if item.strip()]  # Удаляем пустые строки
    listbox.delete(0, tk.END)
    for item in non_empty_items:
        listbox.insert(tk.END, item)

# Функция для сортировки содержимого Listbox
def sort_content():
    global sort_method, sort_order
    items = listbox.get(0, tk.END)
    
    if sort_method == "length":
        sorted_items = sorted(items, key=len, reverse=(sort_order == "descending"))  # Сортировка по длине строк
    elif sort_method == "alphabetical":
        sorted_items = sorted(items, reverse=(sort_order == "descending"))  # Сортировка по алфавиту
    
    listbox.delete(0, tk.END)
    for item in sorted_items:
        listbox.insert(tk.END, item)

# Функция для сохранения отсортированных данных в файл
def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All files", "*.*")],
                                            title="Сохранить файл")
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                items = listbox.get(0, tk.END)
                for item in items:
                    file.write(item + "\n")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

# Функция для переключения метода сортировки
def toggle_sort_method():
    global sort_method
    sort_method = "alphabetical" if sort_method == "length" else "length"
    sort_button.config(text=f"Сортировать по {'алфавиту' if sort_method == 'alphabetical' else 'размеру'}")
    sort_content()

# Функция для переключения порядка сортировки
def toggle_sort_order():
    global sort_order
    sort_order = "descending" if sort_order == "ascending" else "ascending"
    order_button.config(text=f"Порядок сортировки: {'Убывание' if sort_order == 'descending' else 'Возрастание'}")
    sort_content()

# Создаем основное окно
root = tk.Tk()
root.title("Работа с файлами")
root.geometry("800x400")

# Создаем Listbox для отображения содержимого файла
listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

# Создаем кнопки для различных действий
open_button = tk.Button(root, text="Открыть файл", command=open_file)
open_button.pack(side=tk.LEFT, padx=10, pady=10)

sort_button = tk.Button(root, text="Сортировать по размеру", command=toggle_sort_method)
sort_button.pack(side=tk.LEFT, padx=10, pady=10)

order_button = tk.Button(root, text="Порядок сортировки: Возрастание", command=toggle_sort_order)
order_button.pack(side=tk.LEFT, padx=10, pady=10)

remove_empty_button = tk.Button(root, text="Удалить пустые строки", command=remove_empty_lines)
remove_empty_button.pack(side=tk.LEFT, padx=10, pady=10)

save_button = tk.Button(root, text="Сохранить файл", command=save_file)
save_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Запускаем основной цикл приложения
root.mainloop()
