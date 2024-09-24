import tkinter as tk
from threading import Thread, Lock
import time

mutex = Lock()

def delete_words_starting_with(text, letters):
    words = text.split()
    filtered_words = [word for word in words if not word.lower().startswith(tuple(letters))]
    return ' '.join(filtered_words)

def reverse_text(text):
    return text[::-1]

def count_words(text):
    words = text.split()
    return len(words)

def log_message(message):
    log_box.insert(tk.END, message + '\n')
    log_box.see(tk.END)  

def writer1():
    while True:
        mutex.acquire()
        try:
            text = entry.get()
            letters = entry_letters.get().split(",")
            if text:
                result = delete_words_starting_with(text, letters)
                entry.delete(0, tk.END)
                entry.insert(0, result)
                log_message("Писатель 1 удалил слова, начинающиеся с указанных букв.")
                time.sleep(1)
        finally:
            mutex.release()
        time.sleep(5)

def writer2():
    while True:
        mutex.acquire()
        try:
            text = entry.get()
            if text:
                result = reverse_text(text)
                entry.delete(0, tk.END)
                entry.insert(0, result)
                log_message("Писатель 2 изменил порядок символов на обратный.")
                time.sleep(1)
        finally:
            mutex.release()
        time.sleep(7)

def reader1():
    while True:
        mutex.acquire()
        try:
            text = entry.get()
            if text:
                log_message(f"Читатель 1 прочитал текст: {text}")
                time.sleep(1)
        finally:
            mutex.release()
        time.sleep(10)

def reader2():
    while True:
        mutex.acquire()
        try:
            text = entry.get()
            if text:
                word_count = count_words(text)
                log_message(f"Читатель 2 прочитал текст и подсчитал количество слов: {word_count}")
                time.sleep(1)
        finally:
            mutex.release()
        time.sleep(6)

def start_threads():
    Thread(target=writer1).start()
    Thread(target=writer2).start()
    Thread(target=reader2).start()
    Thread(target=reader1).start()

root = tk.Tk()
root.title("Лабораторная работа по потокам")
root.geometry("600x500")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

entry_letters = tk.Entry(root, width=50)
entry_letters.insert(0, "a,b")
entry_letters.pack(pady=10)

log_box = tk.Text(root, height=10, width=70, state=tk.NORMAL)
log_box.pack(pady=10)

start_button = tk.Button(root, text="Запустить потоки", command=start_threads)
start_button.pack(pady=20)

root.mainloop()
