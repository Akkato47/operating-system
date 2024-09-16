import tkinter as tk
from tkinter import messagebox
from threading import Thread

def delete_words_starting_with(text, letters):
    words = text.split()
    filtered_words = [word for word in words if not word.lower().startswith(tuple(letters))]
    return ' '.join(filtered_words)

def reverse_text(text):
    return text[::-1]

def count_words(text):
    words = text.split()
    return len(words)

def delete_every_second_char(text):
    return text[::2]

# Функция для обработки потока
def process_task(task_num):
    text = entry.get()
    letters = entry_letters.get().split(",")  # Получаем буквы, разделённые запятыми
    
    if task_num == 1:
        # Удалить слова, начинающиеся с букв, введённых пользователем
        result = delete_words_starting_with(text, letters)
        entry.delete(0, tk.END)
        entry.insert(0, result)
        
    elif task_num == 2:
        # Записать символы в обратном порядке
        result = reverse_text(text)
        entry.delete(0, tk.END)
        entry.insert(0, result)
        
    elif task_num == 3:
        # Подсчитать количество слов и показать в messagebox
        result = count_words(text)
        messagebox.showinfo("Количество слов", f"Количество слов: {result}")

def on_button_click(task_num):
    Thread(target=process_task, args=(task_num,)).start()

# Создание окна
root = tk.Tk()
root.title("Лабораторная работа по потокам")
root.geometry("500x250")

# Текстовое поле для основного ввода
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Поле для ввода букв
entry_letters = tk.Entry(root, width=50)
entry_letters.insert(0, "a,b")  # Пример, как вводить буквы
entry_letters.pack(pady=10)

# Кнопки для запуска каждого задания
btn_task1 = tk.Button(root, text="Задание 1: Удалить слова, начинающиеся с указанных букв", command=lambda: on_button_click(1))
btn_task1.pack(pady=5)

btn_task2 = tk.Button(root, text="Задание 2: Записать символы в обратном порядке", command=lambda: on_button_click(2))
btn_task2.pack(pady=5)

btn_task3 = tk.Button(root, text="Задание 3: Подсчитать количество слов", command=lambda: on_button_click(3))
btn_task3.pack(pady=5)

# Запуск основного цикла окна
root.mainloop()
