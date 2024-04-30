import tkinter as tk
from tkinter import ttk
import pandas as pd
from config.warehouse_config import get_db_engine
from services import eda


class DataAnalysisApp(tk.Frame):
    def __init__(self, master, data):
        super().__init__(master)
        self.master = master
        self.data = data
        self.eda = eda.EDA(data)  # Instancia de la clase EDA

        # Configura la ventana principal
        self.master.title("SIO - Prac2")
        self.pack(fill=tk.BOTH, expand=True)

        # Crea los widgets de la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Botón para mostrar el histograma
        self.histogram_button = ttk.Button(self, text="Mostrar Histograma de IMDB Score", command=self.show_histogram)
        self.histogram_button.pack(pady=5)

        # Botón para mostrar el mapa de calor
        self.heatmap_button = ttk.Button(self, text="Mostrar Mapa de Calor", command=self.show_heatmap)
        self.heatmap_button.pack(pady=5)

        # Botón para mostrar el scatter plot
        self.scatter_button = ttk.Button(self, text="Mostrar Scatter Plot", command=self.show_scatter)
        self.scatter_button.pack(pady=5)

        # Botón para mostrar el gráfico de violín
        self.violin_button = ttk.Button(self, text="Mostrar Gráfico de Violín", command=self.show_violin)
        self.violin_button.pack(pady=5)

        # Botón para mostrar la matriz de correlación
        self.correlation_button = ttk.Button(self, text="Mostrar Matriz de Correlación",
                                             command=self.show_correlation_matrix)
        self.correlation_button.pack(pady=5)

        # Botón para mostrar la distribución
        self.distribution_button = ttk.Button(self, text="Mostrar Distribución de IMDB Score",
                                              command=self.show_distribution)
        self.distribution_button.pack(pady=5)

    def show_histogram(self):
        self.eda.plot_histogram('imdb_score', bins=15)

    def show_heatmap(self):
        self.eda.plot_heatmap(['imdb_score', 'type'], "Mapa de Calor")

    def show_scatter(self):
        self.eda.plot_scatter('imdb_score', 'release_year', "Scatter Puntuación-Votos")

    def show_violin(self):
        self.eda.plot_violin('imdb_score', "Gráfico de Violín")

    def show_correlation_matrix(self):
        self.eda.plot_correlation_matrix()

    def show_distribution(self):
        self.eda.plot_distribution('imdb_score')


if __name__ == "__main__":
    # Cargamos el DataFrame con las datos
    data = pd.read_sql('SELECT * FROM titles LIMIT 100', get_db_engine())
    data.set_index('id', inplace=True)

    root = tk.Tk()  # Creamos la ventana principal
    app = DataAnalysisApp(root, data)
    root.mainloop() # Iniciamos la aplicación
