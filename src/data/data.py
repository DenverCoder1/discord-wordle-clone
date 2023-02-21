import pandas as pd
import unicodedata

pokemon = pd.read_csv('src/data/csv/pokemon.csv')
pokemon['is_default'] = pokemon['is_default'].astype(bool)

df_species_names = pd.read_csv('src/data/csv/pokemon_species_names.csv')
spanish = df_species_names['local_language_id'] == 7
df_species_names = df_species_names[spanish]
df_species_names = df_species_names[['pokemon_species_id', 'name']]
df_species_names.rename(columns={'name':'Name'}, inplace=True)

pokemon = pd.merge(pokemon, df_species_names, left_on='species_id', right_on='pokemon_species_id')
pokemon.to_csv('pokemon.csv')


def remove_accents(input_str):
    return ''.join(c for c in unicodedata.normalize('NFD', input_str)
                   if unicodedata.category(c) != 'Mn')


def remove_special_char(input_str: str):
    return input_str.replace('’', '').replace('♀', '').replace('♂', '').replace('.', '')


pokemon_names = pokemon['Name'].str.lower().map(remove_special_char).map(remove_accents).to_list()