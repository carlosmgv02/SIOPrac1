import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class EDA:
    def __init__(self, data):
        """
        Inicialitza la classe EDA amb un DataFrame de Pandas.

        :param data: DataFrame de Pandas amb les dades.
        """
        self.data = data

    def descriptive_statistics(self):
        """
        Calcula estadístiques descriptives com la mitjana, la mediana, etc.

        :return: DataFrame amb estadístiques descriptives.
        """
        return self.data.describe()

    def missing_values(self):
        """
        Identifica valors perduts en el DataFrame.

        :return: DataFrame amb el recompte de valors perduts per columna.
        """
        return self.data.isnull().sum()

    def plot_histogram(self, column, bins=10):
        """
        Ploteja un histograma per a una columna específica.

        :param column: Nom de la columna.
        :param bins: Nombre de bins per al histograma.
        """
        self.data[column].hist(bins=bins)
        plt.title(f'Histograma de {column}')
        plt.xlabel(column)
        plt.ylabel('Freqüència')
        plt.show()

    def plot_boxplot(self, column):
        """
        Ploteja un boxplot per a una columna específica.

        :param column: Nom de la columna.
        """
        sns.boxplot(x=self.data[column])
        plt.title(f'Boxplot de {column}')
        plt.xlabel(column)
        plt.show()

    def correlation_matrix(self):
        """
        Calcula la matriu de correlació de les variables numèriques.

        :return: DataFrame amb la matriu de correlació.
        """
        return self.data.corr()

    def plot_correlation_matrix(self):
        """
        Ploteja la matriu de correlació de les variables numèriques.
        """
        corr = self.data.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        plt.title('Matriu de correlació')
        plt.show()

    def value_counts(self, column):
        """
        Calcula el recompte de valors únics en una columna.

        :param column: Nom de la columna.
        :return: DataFrame amb el recompte de valors únics.
        """
        return self.data[column].value_counts()

    def plot_distribution(self, column):
        """
        Ploteja la distribució d'una columna.

        :param column: Nom de la columna.
        """
        sns.kdeplot(self.data[column], shade=True)
        plt.title(f'Distribució de {column}')
        plt.xlabel(column)
        plt.show()
