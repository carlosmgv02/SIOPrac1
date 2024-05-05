import tkinter as tk
from tkinter import ttk
from utils.textUtils import upperCaseFirstLetter
from model.warehouse import session, User, UserPreferences, Genres, AgeCertifications, Platforms
import tkinter.messagebox as tkmessagebox

class UserPreferencesManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Configurar Preferencias")
        self.master.geometry("450x400")
        self.setup_ui()

    def setup_ui(self):
        # Get genres, certifications, and platforms from the database
        genres = [upperCaseFirstLetter(genre.name) for genre in session.query(Genres).all()]
        certifications = [upperCaseFirstLetter(cert.name) for cert in session.query(AgeCertifications).all()]
        platforms = [upperCaseFirstLetter(platform.name) for platform in session.query(Platforms).all()]

        # Campos de configuración (Tipo Preferido, Género, etc.)
        labels_texts = ["Nombre de Usuario:", "Tipo Preferido:", "Género Favorito:", "Certificación de Edad Preferida:",
                        "Duración Mínima (minutos):", "Duración Máxima (minutos):", "Plataforma Favorita:"]
        attributes = ['user_name', 'type', 'genre', 'certification', 'min_duration', 'max_duration', 'platform']
        values = [' ', ["MOVIE", "SHOW"], genres, certifications, None, None, platforms]
        self.vars = {}

        for i, (label_text, attribute, value) in enumerate(zip(labels_texts, attributes, values)):
            tk.Label(self.master, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            if value:
                if attribute == 'user_name':
                    self.vars[attribute] = tk.StringVar()
                    entry = ttk.Entry(self.master, textvariable=self.vars[attribute])
                    entry.grid(row=i, column=1, padx=10, pady=5)
                    # Configurar un evento para activar load_preferences después de que el usuario deje de escribir
                    entry.bind("<KeyRelease>", self.debouncer(self.load_preferences, 500))
                else:
                    self.vars[attribute] = tk.StringVar()
                    ttk.Combobox(self.master, textvariable=self.vars[attribute], values=value, state='readonly').grid(row=i,
                                                                                                                      column=1,
                                                                                                                      padx=10,
                                                                                                                      pady=5)
            else:
                self.vars[attribute] = tk.IntVar()
                ttk.Entry(self.master, textvariable=self.vars[attribute]).grid(row=i, column=1, padx=10, pady=5)

        ttk.Button(self.master, text="Guardar Preferencias", command=self.save_preferences).grid(row=7, column=0,
                                                                                                 columnspan=2, pady=10)

        # Cargar preferencias si existen
        self.load_preferences()

    def save_preferences(self):
        # Obtener el nombre del usuario ingresado
        user_name = self.vars['user_name'].get()
        if not user_name:
            tkmessagebox.showerror("Error", "Por favor, introduce tu nombre de usuario.")
            return

        # Verificar si el usuario ya existe en la base de datos
        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            # Si el usuario no existe, crear uno nuevo
            user = User(name=user_name)
            session.add(user)
            session.flush()  # Flush para obtener el user_id si es necesario inmediatamente

        # Obtener el ID del usuario
        user_id = user.id

        # Verificar si el usuario ya tiene preferencias
        preferences = session.query(UserPreferences).filter_by(user_id=user_id).first()

        # Si el usuario tiene preferencias, actualizarlas; de lo contrario, crear nuevas preferencias
        if preferences:
            preferences.preferred_type = self.vars['type'].get()
            preferences.favorite_genre_id = session.query(Genres).filter(Genres.name.ilike(self.vars['genre'].get())).first().id
            preferences.preferred_certification_id = session.query(AgeCertifications).filter(AgeCertifications.name.ilike(self.vars['certification'].get())).first().id
            preferences.preferred_platform_id = session.query(Platforms).filter(Platforms.name.ilike(self.vars['platform'].get())).first().id
            preferences.preferred_duration_min = int(self.vars['min_duration'].get())
            preferences.preferred_duration_max = int(self.vars['max_duration'].get())
        else:
            preferences = UserPreferences(
                user_id=user_id,
                preferred_type=self.vars['type'].get(),
                favorite_genre_id=session.query(Genres).filter(Genres.name.ilike(self.vars['genre'].get())).first().id,
                preferred_certification_id=session.query(AgeCertifications).filter(AgeCertifications.name.ilike(self.vars['certification'].get())).first().id,
                preferred_platform_id=session.query(Platforms).filter(Platforms.name.ilike(self.vars['platform'].get())).first().id,
                preferred_duration_min=int(self.vars['min_duration'].get()),
                preferred_duration_max=int(self.vars['max_duration'].get())
            )
            session.add(preferences)

        # Guardar cambios en la base de datos
        try:
            session.commit()
            tkmessagebox.showinfo("Guardar Preferencias", "Preferencias guardadas exitosamente.")
            self.clean_preferences()
            self.vars['user_name'].set('')
        except Exception as e:
            session.rollback()
            tkmessagebox.showerror("Error", "Error al guardar las preferencias. Por favor, inténtalo de nuevo.")

    def clean_preferences(self):
        for key in self.vars:
            if key != 'user_name':
                self.vars[key].set('')

    def load_preferences(self, event=None):
        # Obtener el nombre del usuario ingresado
        user_name = self.vars['user_name'].get()
        if user_name:
            # Verificar si el usuario ya existe en la base de datos
            user = session.query(User).filter_by(name=user_name).first()
            if user:
                # Obtener las preferencias del usuario si existen
                preferences = session.query(UserPreferences).filter_by(user_id=user.id).first()
                if preferences:
                    # Cargar las preferencias en los campos de entrada
                    self.vars['type'].set(preferences.preferred_type)
                    self.vars['genre'].set(preferences.favorite_genre.name)
                    self.vars['certification'].set(preferences.preferred_certification.name)
                    self.vars['platform'].set(preferences.preferred_platform.name)
                    self.vars['min_duration'].set(preferences.preferred_duration_min)
                    self.vars['max_duration'].set(preferences.preferred_duration_max)
            else:
                self.clean_preferences()

    def debouncer(self, func, wait_ms=500):
        """Retorna un decorador que retrasa la ejecución de la función `func`."""
        def debounced(*args, **kwargs):
            self.master.after(wait_ms, func, *args, **kwargs)
        return debounced