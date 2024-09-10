import tkinter as tk
from tkinter import filedialog, messagebox

sort_method = "length"
sort_order = "ascending"

def open_file():
    filetypes = [("Text Files", "*.txt"), ("All files", "*.*")]
    filepath = filedialog.askopenfilename(title="Open File", filetypes=filetypes)
    
    if filepath:
        encodings = ['utf-8', 'windows-1251', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                    listbox.delete(0, tk.END)
                    for line in lines:
                        listbox.insert(tk.END, line.strip())
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")
                break

def remove_empty_lines():
    items = listbox.get(0, tk.END)
    non_empty_items = [item for item in items if item.strip()]
    listbox.delete(0, tk.END)
    for item in non_empty_items:
        listbox.insert(tk.END, item)

def sort_content():
    global sort_order
    items = listbox.get(0, tk.END)
    sorted_items = sorted(items, key=len, reverse=(sort_order == "descending"))
    
    listbox.delete(0, tk.END)
    for item in sorted_items:
        listbox.insert(tk.END, item)

def save_file():
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text Files", "*.txt"), ("All files", "*.*")],
                                            title="Save File")
    if filepath:
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                items = listbox.get(0, tk.END)
                for item in items:
                    file.write(item + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def toggle_sort_order():
    global sort_order
    sort_order = "descending" if sort_order == "ascending" else "ascending"
    order_button.config(text=f"Sort Order: {'Descending' if sort_order == 'descending' else 'Ascending'}")
    sort_content()

root = tk.Tk()
root.title("File Manager")
root.geometry("800x600")
root.config(bg="#2c3e50")

listbox = tk.Listbox(root, width=80, height=20, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 12), selectbackground="#3498db")
listbox.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=10)

open_button = tk.Button(button_frame, text="Open File", command=open_file, bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
open_button.grid(row=0, column=0, padx=5)

order_button = tk.Button(button_frame, text="Sort Order: Ascending", command=toggle_sort_order, bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
order_button.grid(row=0, column=1, padx=5)

remove_empty_button = tk.Button(button_frame, text="Remove Empty Lines", command=remove_empty_lines, bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
remove_empty_button.grid(row=0, column=2, padx=5)

save_button = tk.Button(root, text="Save File", command=save_file, bg="green", fg="white", font=("Helvetica", 10, "bold"), padx=10, pady=5)
save_button.pack(side=tk.RIGHT, padx=20, pady=10)

root.mainloop()
