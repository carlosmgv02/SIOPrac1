import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    def __init__(self, data):
        """
        Inicializa la clase EDA con un DataFrame de Pandas.
        """
        self.data = data

    def clean_numeric(self, column):
        """
        Intenta convertir una columna a numérico y maneja las excepciones remplazando
        valores no convertibles con NaN.
        """
        self.data[column] = pd.to_numeric(self.data[column], errors='coerce')

    def descriptive_statistics(self):
        """
        Calcula estadísticas descriptivas como la media, la mediana, etc.
        """
        # Asegúrate de que todas las columnas numéricas sean de tipo adecuado
        for col in self.data.select_dtypes(include=['object']).columns:
            self.clean_numeric(col)
        return self.data.describe()

    def missing_values(self):
        """
        Identifica valores perdidos en el DataFrame.
        """
        return self.data.isnull().sum()

    def plot_histogram(self, column, bins=10):
        """
        Plotea un histograma para una columna específica.
        """
        self.clean_numeric(column)  # Limpia y convierte la columna
        self.data[column].dropna().hist(bins=bins)
        plt.title(f'Histograma de {column}')
        plt.xlabel(column)
        plt.ylabel('Frecuencia')
        plt.show()

    def plot_boxplot(self, column):
        """
        Plotea un boxplot para una columna específica.
        """
        self.clean_numeric(column)  # Limpia y convierte la columna
        sns.boxplot(x=self.data[column].dropna())
        plt.title(f'Boxplot de {column}')
        plt.xlabel(column)
        plt.show()

    def correlation_matrix(self):
        """
        Calcula la matriz de correlación de las variables numéricas.
        """
        # Asegúrate de que todas las columnas numéricas sean de tipo adecuado
        for col in self.data.columns:
            self.clean_numeric(col)
        return self.data.corr()

    def plot_correlation_matrix(self):
        """
        Plotea la matriz de correlación de las variables numéricas.
        """
        corr = self.correlation_matrix()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Matriz de correlación')
        plt.show()

    def value_counts(self, column):
        """
        Calcula el recuento de valores únicos en una columna.
        """
        return self.data[column].value_counts()

    def plot_distribution(self, column):
        """
        Plotea la distribución de una columna.
        """
        self.clean_numeric(column)  # Limpia y convierte la columna
        sns.kdeplot(self.data[column].dropna(), shade=True)
        plt.title(f'Distribución de {column}')
        plt.xlabel(column)
        plt.show()

    def plot_heatmap(self, columns, title):
        """
        Crea un mapa de calor para las correlaciones entre las columnas especificadas.

        :param columns: Lista de nombres de columnas a considerar.
        :param title: Título del mapa de calor.
        """
        for col in columns:
            self.clean_numeric(col)
        corr_matrix = self.data[columns].corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
        plt.title(title)
        plt.show()

    def plot_scatter(self, x, y, title):
        """
        Crea un diagrama de dispersión entre dos columnas especificadas.

        :param x: Nombre de la columna para el eje x.
        :param y: Nombre de la columna para el eje y.
        :param title: Título del gráfico.
        """
        plt.figure(figsize=(8, 6))
        sns.scatterplot(data=self.data, x=x, y=y)
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()

    def plot_bar(self, column, title):
        """
        Crea un gráfico de barras para la columna especificada.

        :param column: Nombre de la columna a graficar.
        :param title: Título del gráfico.
        """
        plt.figure(figsize=(10, 6))
        sns.countplot(data=self.data, x=column)
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel('Frecuencia')
        plt.show()

    def plot_boxplot(self, column, title):
        """
        Crea un boxplot (diagrama de cajas) para la columna especificada.

        :param column: Nombre de la columna a graficar.
        :param title: Título del gráfico.
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.data, x=column)
        plt.title(title)
        plt.show()

    def plot_violin(self, column, title):
        """
        Crea un gráfico de violín para la columna especificada.

        :param column: Nombre de la columna a graficar.
        :param title: Título del gráfico.
        """
        plt.figure(figsize=(10, 6))
        sns.violinplot(data=self.data, x=column)
        plt.title(title)
        plt.show()

    def plot_line(self, x, y, title):
        """
        Crea un gráfico de línea entre dos columnas especificadas.

        :param x: Nombre de la columna para el eje x.
        :param y: Nombre de la columna para el eje y.
        :param title: Título del gráfico.
        """
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=self.data, x=x, y=y)
        plt.title(title)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.show()
