import tkinter as tk
from tkinter import ttk
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from config.warehouse_config import get_db_engine
from services import eda

class DataAnalysisApp(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.master = master
        self.data = data
        self.eda = eda.EDA(data)  # Instancia de la clase EDA

        self.master.title("SIO - Prac2")
        self.pack(fill=tk.BOTH, expand=True)

        self.menu_frame = tk.Frame(self, bd=2, padx=5, pady=5, relief=tk.RAISED)
        self.menu_frame.pack(fill=tk.Y, side=tk.LEFT, expand=False)

        self.graph_frame = tk.Frame(self, bd=2, padx=5, pady=5, relief=tk.RAISED)
        self.graph_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.create_widgets()

    def create_widgets(self):
        buttons_info = [
            ("Histograma de IMDB Score", self.show_histogram),
            ("Mapa de Calor", self.show_heatmap),
            ("Scatter Plot", self.show_scatter),
            ("Gráfico de Violín", self.show_violin),
            ("Matriz de Correlación", self.show_correlation_matrix),
            ("Distribución de IMDB Score", self.show_distribution)
        ]

        for text, command in buttons_info:
            button = ttk.Button(self.menu_frame, text=text, command=command)
            button.pack(fill=tk.X, pady=2)

    def show_graph(self, plot_func, *args, **kwargs):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        plot_func(ax, *args, **kwargs)
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def show_histogram(self):
        self.show_graph(self.eda.plot_histogram, ['imdb_score', 'type'], bins=10)

    def show_heatmap(self):
        self.show_graph(self.eda.plot_heatmap, ['imdb_score', 'type'], title="Mapa de Calor")

    def show_scatter(self):
        self.show_graph(self.eda.plot_scatter, 'imdb_score', 'release_year', title="Scatter Puntuación-Votos")

    def show_violin(self):
        self.show_graph(self.eda.plot_violin, 'imdb_score', title="Gráfico de Violín")

    def show_correlation_matrix(self):
        self.show_graph(self.eda.plot_correlation_matrix)

    def show_distribution(self):
        self.show_graph(self.eda.plot_distribution, 'imdb_score')

if __name__ == "__main__":
    data = pd.read_sql('SELECT * FROM titles LIMIT 100', get_db_engine())
    data.set_index('id', inplace=True)

    root = tk.Tk()
    app = DataAnalysisApp(root, data)
    root.mainloop()
