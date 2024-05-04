import tkinter as tk
from tkinter import ttk

GENRES = ['Acción', 'Comedia', 'Drama', 'Fantasía', 'Horror']
CERTIFICATIONS = ['G', 'PG', 'PG-13', 'R', 'NC-17']
PLATFORMS = ['Netflix', 'Hulu', 'Disney+', 'HBO', 'Amazon Prime']


class UserPreferencesManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Configurar Preferencias")
        self.master.geometry("400x400")
        self.setup_ui()

    def setup_ui(self):
        # Campos de configuración (Tipo Preferido, Género, etc.)
        labels_texts = ["Tipo Preferido:", "Género Favorito:", "Certificación de Edad Preferida:",
                        "Duración Mínima (minutos):", "Duración Máxima (minutos):", "Plataforma Favorita:"]
        attributes = ['type', 'genre', 'certification', 'min_duration', 'max_duration', 'platform']
        values = [["MOVIE", "SHOW"], GENRES, CERTIFICATIONS, None, None, PLATFORMS]
        self.vars = {}

        for i, (label_text, attribute, value) in enumerate(zip(labels_texts, attributes, values)):
            tk.Label(self.master, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            if value:
                self.vars[attribute] = tk.StringVar()
                ttk.Combobox(self.master, textvariable=self.vars[attribute], values=value, state='readonly').grid(row=i,
                                                                                                                  column=1,
                                                                                                                  padx=10,
                                                                                                                  pady=5)
            else:
                self.vars[attribute] = tk.IntVar()
                ttk.Entry(self.master, textvariable=self.vars[attribute]).grid(row=i, column=1, padx=10, pady=5)

        ttk.Button(self.master, text="Guardar Preferencias", command=self.save_preferences).grid(row=6, column=0,
                                                                                                 columnspan=2, pady=10)

    def save_preferences(self):
        # Aquí podría ir el código para guardar las preferencias en una base de datos o archivo
        for attribute, var in self.vars.items():
            print(f"{attribute.capitalize()}: {var.get()}")
