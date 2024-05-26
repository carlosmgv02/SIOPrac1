import geopandas as gpd
import pandas as pd
import plotly.express as px
from config.warehouse_config import get_db_engine
from data_cleaner import DataCleaner

data_cleaner = DataCleaner('GIS/countries.geojson', 'GIS/continents.geojson', 'GIS/capitals.csv')

def fetch_data(query):
    engine = get_db_engine()
    df = pd.read_sql(query, engine)
    df['country_code'] = df['country_code'].apply(lambda x: data_cleaner.convert_code(x))
    return df

def generate_map(df, color_field, html_file_name, color_scale="Viridis"):
    gdf_countries = gpd.read_file('countries.geojson')
    df_merged = gdf_countries.merge(df, left_on='ISO_A3', right_on='country_code', how='left')
    df_merged[color_field] = df_merged[color_field].fillna(0)
    fig = px.choropleth(
        df_merged,
        geojson=df_merged.geometry.__geo_interface__,
        locations=df_merged.index,
        color=color_field,
        color_continuous_scale=color_scale,
        hover_data=["ADMIN"]
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.write_html(f"templates/{html_file_name}.html")

def generate_movie_count_map():
    query = """
    SELECT pc.country_code, COUNT(*) AS number_of_movies
    FROM public.titlecountries tc
    JOIN public.productioncountries pc ON tc.country_id = pc.id
    GROUP BY pc.country_code
    ORDER BY number_of_movies DESC;
    """
    df = fetch_data(query)
    generate_map(df, "number_of_movies", "heatmap", "RdBu")

def generate_genre_count_map():
    query = """
    SELECT pc.country_code, COUNT(DISTINCT tg.genre_id) AS number_of_genres
    FROM public.titlegenres tg
    JOIN public.titles t ON tg.title_id = t.id
    JOIN public.titlecountries tc ON t.id = tc.title_id
    JOIN public.productioncountries pc ON tc.country_id = pc.id
    GROUP BY pc.country_code
    ORDER BY number_of_genres DESC;
    """
    df = fetch_data(query)
    generate_map(df, "number_of_genres", "genre_heatmap", "Viridis")


def fetch_data_with_capitals():
    # Loading capital data
    capitals_df = pd.read_csv('capitals.csv', delimiter=';')

    # Query to fetch movies or genres data
    query = """
    SELECT pc.country_code as COUNTRY_CODE, COUNT(DISTINCT tg.genre_id) AS number_of_genres
    FROM public.titlegenres tg
    JOIN public.titles t ON tg.title_id = t.id
    JOIN public.titlecountries tc ON t.id = tc.title_id
    JOIN public.productioncountries pc ON tc.country_id = pc.id
    GROUP BY pc.country_code
    ORDER BY number_of_genres DESC;
    """
    engine = get_db_engine()
    genres_df = pd.read_sql(query, engine)
    genres_df.columns = [x.upper().strip() for x in genres_df.columns]
    # Merge genres data with capitals data on country_code
    merged_df = pd.merge(genres_df, capitals_df, on='COUNTRY_CODE', how='left')
    return merged_df


def generate_capital_based_map():
    df = fetch_data_with_capitals()

    fig = px.scatter_geo(
        df,
        lat='LATITUDE',
        lon='LONGITUDE',
        text='CAPITAL',
        size='NUMBER_OF_GENRES',  # Adjusted to match the exact column name case
        color='NUMBER_OF_GENRES',  # Assuming you might also want to use color for the same data
        hover_name='CAPITAL',
        projection='natural earth',
        title='Number of Genres by Capital City'
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(showland=True, landcolor="LightGreen", showcountries=True)
    )
    fig.write_html("templates/capital_genre_map.html")