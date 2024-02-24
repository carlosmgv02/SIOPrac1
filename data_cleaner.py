import pandas as pd
import ast


def clean_list(value):
    if pd.isna(value) or value == "[]":
        return []
    try:
        return eval(value)
    except:
        return []


def convert_to_initials(country_name):
    if len(country_name) > 10:
        initials = ''.join([word[0] for word in country_name.split()])
        return initials.upper()
    else:
        return country_name
