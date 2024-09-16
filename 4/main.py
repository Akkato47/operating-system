import tkinter as tk
from threading import Thread, Lock
import time

# Мьютекс для синхронизации доступа к общему ресурсу
mutex = Lock()

# Общий разделяемый ресурс
shared_resource = "text"

# Функция для вывода логов в текстовое поле
def log_message(message):
    log_box.insert(tk.END, message + '\n')
    log_box.see(tk.END)  # Автопрокрутка до конца

# Функция для писателей
def writer(writer_id):
    global shared_resource
    while True:
        mutex.acquire()
        try:
            # Писатель записывает данные в общий ресурс
            shared_resource = f"Данные от писателя {writer_id}"
            text_writer[writer_id].config(text=shared_resource)
            log_message(f"Писатель {writer_id} записал: {shared_resource}")
        finally:
            mutex.release()
        time.sleep(2)  # Имитация паузы

# Функция для читателей
def reader(reader_id):
    global shared_resource
    while True:
        mutex.acquire()
        try:
            # Читатель читает данные из общего ресурса
            read_data = shared_resource
            text_reader[reader_id].config(text=read_data)
            log_message(f"Читатель {reader_id} прочитал: {read_data}")
            # После прочтения данные удаляются
            shared_resource = ""
        finally:
            mutex.release()
        time.sleep(2)  # Имитация паузы

# Создание потоков для писателей и читателей
def start_threads():
    for i in range(4):
        writer_thread = Thread(target=writer, args=(i,))
        writer_thread.start()
        reader_thread = Thread(target=reader, args=(i,))
        reader_thread.start()

# Создание окна
root = tk.Tk()
root.title("Писатели и Читатели с мьютексом")
root.geometry("600x600")

# Метки для отображения данных писателей
text_writer = []
for i in range(2):
    label = tk.Label(root, text=f"Писатель {i}: нет данных", width=50, relief="solid")
    label.pack(pady=5)
    text_writer.append(label)

# Метки для отображения данных читателей
text_reader = []
for i in range(2):
    label = tk.Label(root, text=f"Читатель {i}: нет данных", width=50, relief="solid")
    label.pack(pady=5)
    text_reader.append(label)

# Логгер для отображения логов в окне
log_box = tk.Text(root, height=10, width=70, state=tk.NORMAL)
log_box.pack(pady=10)

# Кнопка для запуска потоков
start_button = tk.Button(root, text="Запустить потоки", command=start_threads)
start_button.pack(pady=20)

# Запуск основного цикла окна
root.mainloop()
