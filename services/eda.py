import numpy as np
import pandas as pd


def platform_action_content(data):
    """
    Calcula quina plataforma de streaming té més i menys contingut d'acció.

    :param data: El DataFrame de Pandas amb les dades.
    """
    platform_action_count = data.groupby('platform')['action'].sum()
    platform_action_count = platform_action_count.sort_values(ascending=False)
    most_action_platform = platform_action_count.idxmax()
    least_action_platform = platform_action_count.idxmin()
    return most_action_platform, least_action_platform


def series_movie_distribution(data):
    """
    Calcula la distribució entre sèries i pel·lícules a cada plataforma de streaming.

    :param data: El DataFrame de Pandas amb les dades.
    """
    series_movie_distribution = data.groupby('platform')['type'].value_counts(normalize=True)
    return series_movie_distribution


def top_10_actors(data):
    """
    Troba els deu actors que han protagonitzat més pel·lícules.

    :param data: El DataFrame de Pandas amb les dades.
    """
    top_10_actors = data['actor'].value_counts().head(10)
    return top_10_actors


def multi_platform_content_proportion(data):
    """
    Calcula la proporció de contingut que es troba en més d'una plataforma de streaming.

    :param data: El DataFrame de Pandas amb les dades.
    """
    multi_platform_content = data.groupby('title')['platform'].nunique()
    multi_platform_content_proportion = (multi_platform_content > 1).mean()
    return multi_platform_content_proportion


def genre_distribution(data):
    """
    Calcula la distribució dels gèneres de contingut a cada plataforma de streaming.

    :param data: El DataFrame de Pandas amb les dades.
    """
    genre_distribution = data.groupby('platform')['genre'].value_counts(normalize=True)
    return genre_distribution


def content_rating_distribution(data):
    """
    Calcula la distribució dels rànquings de contingut a cada plataforma de streaming.

    :param data: El DataFrame de Pandas amb les dades.
    """
    content_rating_distribution = data.groupby('platform')['content_rating'].value_counts(normalize=True)
    return content_rating_distribution


def average_runtime(data):
    """
    Calcula la mitjana de la durada de les pel·lícules i sèries a cada plataforma de streaming.

    :param data: El DataFrame de Pandas amb les dades.
    """
    average_runtime = data.groupby('platform')['runtime'].mean()
    return average_runtime


def release_decade_analysis(data):
    """
    Analitza la distribució del contingut en funció de la dècada de llançament.

    :param data: El DataFrame de Pandas amb les dades.
    """
    data['release_decade'] = (data['release_year'] // 10) * 10
    release_decade_analysis = data.groupby('release_decade')['title'].count()
    return release_decade_analysis


def load_data(db_rows):
    pd.read


def main():
    # Carregar les dades
    file_path = 'ruta/al/fitcher.csv'  # Canvia la ruta pel teu fitxer CSV
    data = load_data(file_path)

    while True:
        print("\nMenú:")
        print("1. Quina plataforma de streaming té més i menys contingut d'acció?")
        print("2. Distribució entre sèries i pel·lícules a cada plataforma de streaming")
        print("3. Deu actors que han protagonitzat més pel·lícules")
        print("4. Proporció de contingut que es troba en més d'una plataforma de streaming")
        print("5. Distribució dels gèneres de contingut a cada plataforma de streaming")
        print("6. Distribució dels rànquings de contingut a cada plataforma de streaming")
        print("7. Mitjana de la durada de les pel·lícules i sèries a cada plataforma de streaming")
        print("8. Anàlisi de la distribució del contingut en funció de la dècada de llançament")
        print("9. Sortir")

        option = input("\nSelecciona una opció: ")

        if option == '1':
            most_action_platform, least_action_platform = platform_action_content(data)
            print(f"\nLa plataforma amb més contingut d'acció és: {most_action_platform}")
            print(f"La plataforma amb menys contingut d'acció és: {least_action_platform}")
        elif option == '2':
            print("\nDistribució entre sèries i pel·lícules a cada plataforma de streaming:")
            print(series_movie_distribution(data))
        elif option == '3':
            print("\nDeu actors que han protagonitzat més pel·lícules:")
            print(top_10_actors(data))
        elif option == '4':
            print("\nProporció de contingut que es troba en més d'una plataforma de streaming:")
            print(multi_platform_content_proportion(data))
        elif option == '5':
            print("\nDistribució dels gèneres de contingut a cada plataforma de streaming:")
            print(genre_distribution(data))
        elif option == '6':
            print("\nDistribució dels rànquings de contingut a cada plataforma de streaming:")
            print(content_rating_distribution(data))
        elif option == '7':
            print("\nMitjana de la durada de les pel·lícules i sèries a cada plataforma de streaming:")
            print(average_runtime(data))
        elif option == '8':
            print("\nAnàlisi de la distribució del contingut en funció de la dècada de llançament:")
            print(release_decade_analysis(data))
        elif option == '9':
            print("\nAdéu!")
            break
        else:
            print("\nOpció no vàlida. Si us plau, selecciona una opció vàlida.")


if __name__ == "__main__":
    main()