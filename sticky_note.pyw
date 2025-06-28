import tkinter as tk
import os

NOTE_FILE = "note.txt"
CONFIG_FILE = "config.txt"

THEMES = {
    "yellow": "#FFFACD",
    "pink": "#FFD1DC",
    "blue": "#D0F0FD"
}
current_theme = "yellow"

def save_note(event=None):
    with open(NOTE_FILE, "w", encoding="utf-8") as f:
        f.write(text_area.get("1.0", "end-1c"))

def load_note():
    if os.path.exists(NOTE_FILE):
        with open(NOTE_FILE, "r", encoding="utf-8") as f:
            text_area.insert("1.0", f.read())

def save_theme():
    with open(CONFIG_FILE, "w") as f:
        f.write(current_theme)

def load_theme():
    global current_theme
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            theme = f.read().strip()
            if theme in THEMES:
                current_theme = theme

def apply_theme():
    color = THEMES[current_theme]
    root.configure(bg=color)
    top_bar.configure(bg=color)
    text_area.configure(bg=color)
    for w in top_bar.winfo_children():
        if isinstance(w, tk.Button):
            w.configure(bg=color)

def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    apply_theme()
    save_theme()

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = event.x_root - root.x
    y = event.y_root - root.y
    root.geometry(f"+{x}+{y}")

def close_note():
    root.destroy()

def minimize_note():
    root.iconify()

# Setup single window
load_theme()

root = tk.Tk()
root.title("Sticky Note")
root.geometry("300x300")
root.attributes("-topmost", True)
root.overrideredirect(False)  # Let it keep window manager (taskbar/minimize)
root.iconbitmap('')  # Add 'note.ico' here if you have it

# Top bar with buttons
top_bar = tk.Frame(root, height=25)
top_bar.pack(fill='x', side='top')
top_bar.bind("<Button-1>", start_move)
top_bar.bind("<B1-Motion>", do_move)

tk.Button(top_bar, text="❌", command=close_note, bd=0, font=("Arial", 10), padx=5).pack(side="right")
tk.Button(top_bar, text="🗕", command=minimize_note, bd=0, font=("Arial", 10), padx=5).pack(side="right")
tk.Button(top_bar, text="🩵", command=lambda: set_theme("blue"), bd=0, font=("Arial", 10)).pack(side="right")
tk.Button(top_bar, text="🌸", command=lambda: set_theme("pink"), bd=0, font=("Arial", 10)).pack(side="right")
tk.Button(top_bar, text="🧈", command=lambda: set_theme("yellow"), bd=0, font=("Arial", 10)).pack(side="right")

# Text area
text_area = tk.Text(root, wrap='word', font=("Arial", 12), bd=0)
text_area.pack(expand=True, fill='both', padx=10, pady=5)

apply_theme()
load_note()

root.bind("<Control-s>", save_note)
text_area.bind("<KeyRelease>", save_note)

root.mainloop()
