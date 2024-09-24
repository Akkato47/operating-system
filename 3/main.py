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

def delete_words_containing_letter(text, letter):
    words = text.split()
    filtered_words = [word for word in words if letter.lower() not in word.lower()]
    return ' '.join(filtered_words)

def delete_every_second_char(text):
    return text[::2]

def process_task(task_num):
    text = entry.get()
    letters = entry_letters.get().split(",")
    
    if task_num == 1:
        result = delete_words_starting_with(text, letters)
        entry.delete(0, tk.END)
        entry.insert(0, result)
        
    elif task_num == 2:
        result = reverse_text(text)
        entry.delete(0, tk.END)
        entry.insert(0, result)
        
    elif task_num == 3:
        result = count_words(text)
        messagebox.showinfo("Количество слов", f"Количество слов: {result}")
        
    elif task_num == 4:
        letter = entry_single_letter.get()
        result = delete_words_containing_letter(text, letter)
        entry.delete(0, tk.END)
        entry.insert(0, result)

    elif task_num == 5:
        result = delete_every_second_char(text)
        entry.delete(0, tk.END)
        entry.insert(0, result)

def on_button_click(task_num):
    Thread(target=process_task, args=(task_num,)).start()

root = tk.Tk()
root.title("Лабораторная работа по потокам")
root.geometry("500x300")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

entry_letters = tk.Entry(root, width=50)
entry_letters.insert(0, "a,b")
entry_letters.pack(pady=10)

entry_single_letter = tk.Entry(root, width=50)
entry_single_letter.insert(0, "h")
entry_single_letter.pack(pady=10)

btn_task1 = tk.Button(root, text="Задание 1: Удалить слова, начинающиеся с указанных букв", command=lambda: on_button_click(1))
btn_task1.pack(pady=5)

btn_task2 = tk.Button(root, text="Задание 2: Записать символы в обратном порядке", command=lambda: on_button_click(2))
btn_task2.pack(pady=5)

btn_task3 = tk.Button(root, text="Задание 3: Подсчитать количество слов", command=lambda: on_button_click(3))
btn_task3.pack(pady=5)

btn_task4 = tk.Button(root, text="Задание 4: Удалить слова, содержащие букву", command=lambda: on_button_click(4))
btn_task4.pack(pady=5)

btn_task5 = tk.Button(root, text="Задание 5: Удалить каждый 2-ой символ", command=lambda: on_button_click(5))
btn_task5.pack(pady=5)

root.mainloop()
