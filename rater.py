import tkinter as tk
from tkinter import ttk

from model.warehouse import Titles, session


class AutoCompleteEntry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.var = tk.StringVar()
        self.config(textvariable=self.var)
        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.lb_up = False
        self.titles_dict = {}

    def set_completion_list(self, lista):
        self.lista = sorted(lista, key=str.lower)

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = tk.Listbox()
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
            title_id, title_name = self.titles_dict[self.lb.get(index)]
            self.var.set(title_name)
            print("ID seleccionado:", title_id)
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def move_up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.see(index)  # Scroll!
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
                self.lb.see(index)  # Scroll!
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = self.var.get().lower()
        type_selected = type_var.get()
        results = session.query(Titles.id, Titles.title).filter(Titles.title.ilike(f'%{pattern}%'), Titles.type == type_selected).all()
        self.titles_dict = {title: (title_id, title) for title_id, title in results}
        return results

def update_rating_label(event):
    # Actualizar la etiqueta con la calificación seleccionada.
    rating_label.config(text=f"Rating: {rating_var.get():.1f}")

def test():
    root = tk.Tk()
    root.geometry("300x200")

    global type_var
    type_var = tk.StringVar()
    type_selector = ttk.Combobox(root, textvariable=type_var, values=["MOVIE", "SHOW"], state='readonly')
    type_selector.grid(row=0, column=0, padx=10, pady=10)
    type_selector.set("movie")  # Default value

    entry = AutoCompleteEntry(root)
    entry.grid(row=1, column=0, padx=10, pady=10)

    global rating_var
    rating_var = tk.DoubleVar()
    rating_scale = ttk.Scale(root, from_=1, to=5, variable=rating_var, orient='horizontal', command=update_rating_label)
    rating_scale.grid(row=2, column=0, padx=10, pady=10)

    global rating_label
    rating_label = ttk.Label(root, text="Rating: 1.0")
    rating_label.grid(row=2, column=1, padx=0, pady=10)

    tk.Button(root, text='Salir', command=root.quit).grid(row=3, column=0, pady=10)
    root.mainloop()

test()
