from models import *
import pandas as pd


def extract_provider_name(file_name):
    parts = file_name.rsplit('_', 1)  # Dividir por la última aparición de '_'
    provider_name = parts[0].replace('_', ' ')  # Reemplazar los restantes '_' por espacios
    return provider_name





