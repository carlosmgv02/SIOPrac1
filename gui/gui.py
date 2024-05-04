import tkinter as tk
from tkinter import ttk
from rater import AutoCompleteApp
from user_preferences import UserPreferencesManager

def launch_rate_movie():
    rate_movie_window = tk.Toplevel(root)
    rate_movie_window.title("Valorar Película")
    rate_movie_window.geometry("400x300")
    entry = AutoCompleteApp(rate_movie_window)



def launch_user_preferences():
    user_preferences_window = tk.Toplevel(root)
    UserPreferencesManager(user_preferences_window)

root = tk.Tk()
root.title("Menú Principal")
root.geometry("300x150")

ttk.Button(root, text="Valorar Película", command=launch_rate_movie).pack(pady=10)
ttk.Button(root, text="Configurar Preferencias", command=launch_user_preferences).pack(pady=10)

root.mainloop()
