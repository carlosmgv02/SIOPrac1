import tkinter as tk
from tkinter import ttk
from model.warehouse import Titles, session, UserInteractions, User
import tkinter.messagebox as tkmessagebox


class AutoCompleteApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("350x300")

        self.type_var = tk.StringVar(value="MOVIE")
        self.rating_var = tk.DoubleVar(value=1.0)
        self.user_name_var = tk.StringVar()  # Variable to hold the user's name

        self.setup_widgets()

    def setup_widgets(self):
        ttk.Label(self.root, text="User Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.user_name_var).grid(row=0, column=1, padx=10, pady=10)

        type_selector = ttk.Combobox(self.root, textvariable=self.type_var, values=["MOVIE", "SHOW"], state='readonly')
        type_selector.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        type_selector.set("MOVIE")  # Default value

        self.entry = AutoCompleteEntry(self.root, self.type_var)
        self.entry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        rating_scale = ttk.Scale(self.root, from_=1, to = 5, variable = self.rating_var, orient = 'horizontal', command = self.update_rating_label)
        rating_scale.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.rating_label = ttk.Label(self.root, text="Rating: 1.0")
        self.rating_label.grid(row=3, column=1, padx=0, pady=10)

        tk.Button(self.root, text='Guardar Valoración', command=self.save_rating).grid(row=4, column=0, columnspan=2,
                                                                                       pady=10)
        tk.Button(self.root, text='Salir', command=self.root.quit).grid(row=5, column=0, columnspan=2, pady=10)

    def update_rating_label(self, event):
        self.rating_label.config(text=f"Rating: {self.rating_var.get():.1f}")

    def save_rating(self):
        user_name = self.user_name_var.get()
        if not user_name:
            tk.messagebox.showerror("Error", "Please enter your name.")
            return

        user = session.query(User).filter_by(name=user_name).first()
        if not user:
            confirmation = tkmessagebox.askyesno("User Not Found", "User not found. Do you want to create a new user?")
            if not confirmation:
                return

            user = User(name=user_name)
            session.add(user)
            session.flush()

        if self.entry.selected_title_id:
            interaction = UserInteractions(
                user_id=user.id,
                title_id=self.entry.selected_title_id,
                rating=int(self.rating_var.get()),
                watched=True
            )
            session.add(interaction)
            try:
                session.commit()
                tk.messagebox.showinfo("Guardar Valoración", "Valoración guardada exitosamente.")
                self.restart_inputs()
            except Exception as e:
                session.rollback()

                tk.messagebox.showerror("Error", f"Failed to save rating: {e}")
        else:
            tk.messagebox.showerror("Guardar Valoración", "No se ha seleccionado una película.")
    def restart_inputs(self):
        self.user_name_var.set('')
        self.type_var.set('MOVIE')
        self.rating_var.set(1.0)
        self.entry.var.set('')
        self.entry.selected_title_id = None

class AutoCompleteEntry(ttk.Entry):
    def __init__(self, master, type_var, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.type_var = type_var
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.lb_up = False
        self.titles_dict = {}
        self.selected_title_id = None

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox(self.master)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for w in words:
                    self.lb.insert(tk.END, w[1])  # Insert title name
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        if self.lb_up:
            index = self.lb.curselection()[0]
            self.selected_title_id, title_name = self.titles_dict[self.lb.get(index)]
            self.var.set(title_name)
            self.lb.destroy()
            self.lb_up = False

    def move_up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def move_down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != str(self.lb.size() - 1):
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.see(index)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = self.var.get().lower()
        type_selected = self.type_var.get()
        results = session.query(Titles.id, Titles.title).filter(Titles.title.ilike(f'%{pattern}%'), Titles.type == type_selected).all()
        self.titles_dict = {title: (title_id, title) for title_id, title in results}
        return results


