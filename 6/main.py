import tkinter as tk
from threading import Thread
import time
import random
import queue

# Параметры трассы по умолчанию
track_length = 20 
num_runners = 5  
obstacle_chance = 0.5  
obstacle_delay = 1.5 

event_queue = queue.Queue()

log_window = None
log_box = None
config_win = None

def log_message(message):
    global log_window, log_box
    if log_window is None or not log_window.winfo_exists():
        return
    if log_box and message.strip():
        log_box.insert(tk.END, message + "\n")
        log_box.see(tk.END)

def create_log_window():
    global log_window, log_box
    if log_window is None or not log_window.winfo_exists():
        log_window = tk.Toplevel()
        log_window.title("Логи")
        log_box = tk.Text(log_window, height=20, width=60, state=tk.NORMAL)
        log_box.pack(pady=10)

def runner(runner_id, config):
    track_len, obs_delay = config['track_length'], config['obstacle_delay']
    for position in range(track_len):
        if track[position][runner_id] == 1:
            event_queue.put((runner_id, position, "obstacle"))
            log_message(f"Бегун {runner_id+1} встретил препятствие на позиции {position}. Задержка {obs_delay} секунд.")
            time.sleep(obs_delay)
        else:
            event_queue.put((runner_id, position, "move"))
        time.sleep(0.5)

    event_queue.put((runner_id, track_len - 1, "finish"))
    log_message(f"Бегун {runner_id+1} финишировал!")

def create_track(track_len, num_runners, obs_chance):
    track = [[random.choice([0, 1]) if random.random() < obs_chance else 0 for _ in range(num_runners)] for _ in range(track_len)]
    log_message("Сгенерированный трек:")
    for row in track:
        log_message(" ".join('X' if cell == 1 else '.' for cell in row))
    return track

def start_race(config):
    global track
    track = create_track(config['track_length'], config['num_runners'], config['obstacle_chance'])

    for runner_id in range(config['num_runners']):
        t = Thread(target=runner, args=(runner_id, config))
        t.start()

    root.after(10, update_interface)

def update_interface():
    try:
        while True:
            runner_id, position, event_type = event_queue.get_nowait()
            for i in range(config['track_length']):
                if i == position:
                    if i == config['track_length'] - 1:
                        labels[i][runner_id].config(text="🏁", bg="green")
                    elif event_type == "obstacle":
                        labels[i][runner_id].config(text="🟥", bg="red")
                    elif event_type == "move":
                        labels[i][runner_id].config(text="🏃", bg="white") 
                else:
                    labels[i][runner_id].config(text="⬜", bg="white")
    except queue.Empty:
        pass
    root.after(10, update_interface)

def build_track_interface(root, track_len, num_runners):
    labels = []
    for i in range(track_len):
        row = []
        for j in range(num_runners):
            lbl = tk.Label(root, text="⬜", font=("Helvetica", 10), width=2, height=1, bg="white", relief="solid")
            lbl.grid(row=i, column=j, padx=1, pady=1)
            row.append(lbl)
        labels.append(row)
    return labels

def config_window():
    global config_win
    if config_win is None or not config_win.winfo_exists():
        config_win = tk.Toplevel()
        config_win.title("Конфигурация")
        config_win.geometry("200x200")

        def apply_config():
            try:
                config['track_length'] = int(track_length_entry.get())
                config['num_runners'] = int(num_runners_entry.get())
                config['obstacle_chance'] = float(obstacle_chance_entry.get())
                config['obstacle_delay'] = float(obstacle_delay_entry.get())
                log_message("Конфигурация обновлена.")
                rebuild_interface(config['track_length'], config['num_runners'])
            except ValueError:
                log_message("Ошибка: введите корректные значения.")

        tk.Label(config_win, text="Длина трассы").pack()
        track_length_entry = tk.Entry(config_win)
        track_length_entry.insert(0, str(config['track_length']))
        track_length_entry.pack()

        tk.Label(config_win, text="Количество бегунов").pack()
        num_runners_entry = tk.Entry(config_win)
        num_runners_entry.insert(0, str(config['num_runners']))
        num_runners_entry.pack()

        tk.Label(config_win, text="Шанс препятствия (0-1)").pack()
        obstacle_chance_entry = tk.Entry(config_win)
        obstacle_chance_entry.insert(0, str(config['obstacle_chance']))
        obstacle_chance_entry.pack()

        tk.Label(config_win, text="Задержка на препятствии (сек)").pack()
        obstacle_delay_entry = tk.Entry(config_win)
        obstacle_delay_entry.insert(0, str(config['obstacle_delay']))
        obstacle_delay_entry.pack()

        apply_button = tk.Button(config_win, text="Применить", command=apply_config)
        apply_button.pack(pady=10)

def rebuild_interface(track_len, num_runners):
    global labels
    for widget in root.grid_slaves():
        widget.destroy()
    labels = build_track_interface(root, track_len, num_runners)
    start_button = tk.Button(root, text="Начать гонку", command=lambda: start_race(config))
    start_button.grid(row=track_len, columnspan=num_runners, pady=20)

    log_button = tk.Button(root, text="Показать логи", command=create_log_window)
    log_button.grid(row=track_len + 1, columnspan=num_runners, pady=10)

    config_button = tk.Button(root, text="Конфигурация", command=config_window)
    config_button.grid(row=track_len + 2, columnspan=num_runners, pady=10)

def main_window():
    global root, labels, config
    config = {
        'track_length': track_length,
        'num_runners': num_runners,
        'obstacle_chance': obstacle_chance,
        'obstacle_delay': obstacle_delay
    }

    root = tk.Tk()
    root.title("Бег с препятствиями")
    root.geometry("150x700")

    labels = build_track_interface(root, config['track_length'], config['num_runners'])

    start_button = tk.Button(root, text="Начать гонку", command=lambda: start_race(config))
    start_button.grid(row=config['track_length'], columnspan=config['num_runners'], pady=20)

    log_button = tk.Button(root, text="Показать логи", command=create_log_window)
    log_button.grid(row=config['track_length'] + 1, columnspan=config['num_runners'], pady=10)

    config_button = tk.Button(root, text="Конфигурация", command=config_window)
    config_button.grid(row=config['track_length'] + 2, columnspan=config['num_runners'], pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
