import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import os
import platform

def open_image():
    filetypes = [
        ("Image Files", "*.bmp;*.jpg;*.jpeg;*.gif;*.png"),
        ("All files", "*.*")
    ]
    filepath = filedialog.askopenfilename(title="Open Image", filetypes=filetypes)
    
    if filepath:
        try:
            img = Image.open(filepath)
            img = img.resize((picture_box.winfo_width(), picture_box.winfo_height()), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            picture_box.config(image=img_tk)
            picture_box.image = img_tk
            picture_box.config(bg='#ffffff', borderwidth=0)
            
            filepath_label.config(text=f"File Path: {filepath}")
        except UnidentifiedImageError:
            messagebox.showerror("Error", "Invalid image format. Please choose a valid image file (.png, .jpeg, .bmp, .gif)")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the image: {str(e)}")

def show_system_info():
    info = f"""
    Computer Name: {platform.node()}
    Operating System: {platform.system()} {platform.release()} ({platform.version()})
    Architecture: {platform.machine()}
    Processor: {platform.processor()}
    Platform: {platform.platform()}
    Path to Home Directory: {os.path.expanduser('~')}
    """
    
    messagebox.showinfo("System Information", info)

def on_enter(event, btn):
    btn['background'] = '#4CAF50'
    btn['foreground'] = 'white'

def on_leave(event, btn):
    btn['background'] = '#ffffff'
    btn['foreground'] = 'black'

root = tk.Tk()
root.title("Image Viewer")
root.geometry("800x800")
root.configure(bg='#2c3e50')

frame_bg = tk.Frame(root, bg='#ecf0f1', relief=tk.SUNKEN, borderwidth=5)
frame_bg.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=750, height=550)

picture_box = tk.Label(frame_bg, text="The image will appear here", font=('Arial', 16), bg='#bdc3c7', fg='#7f8c8d', relief=tk.GROOVE, borderwidth=5)
picture_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

filepath_label = tk.Label(root, text="File Path: None", font=('Helvetica', 10), bg='#2c3e50', fg='#ecf0f1')
filepath_label.place(relx=0.5, rely=0.88, anchor=tk.CENTER)

open_button = tk.Button(root, text="Open Image", command=open_image, font=('Helvetica', 12, 'bold'), fg='black', bg='#ffffff', activebackground='#4CAF50', activeforeground='white', borderwidth=0, relief=tk.RAISED)
open_button.place(relx=0.7, rely=0.95, anchor=tk.S, width=150, height=40)

menubar = tk.Menu(root)
system_menu = tk.Menu(menubar, tearoff=0, bg='#bdc3c7', fg='#2c3e50', activebackground='#4CAF50', activeforeground='white')
system_menu.add_command(label="System Information", command=show_system_info)
menubar.add_cascade(label="System", menu=system_menu)
root.config(menu=menubar)

open_button.bind("<Enter>", lambda event: on_enter(event, open_button))
open_button.bind("<Leave>", lambda event: on_leave(event, open_button))

root.minsize(600, 600)
root.maxsize(1200, 1200)

root.mainloop()
