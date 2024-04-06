from pymongo import MongoClient
import csv
import json
import pandas as pd

##pokemon Dict example
pokemon_dict = {
    '_id' : [],
    'p_id' : [],
    'p_avatar': [],
    'p_nme': [],
    'p_types': [],
    'p_ability': [],
    'p_height': [],
    'p_weight': [],
    'p_location': [],
    'p_evostage': [],
    'p_dex_entries': []
}

##to be used ot convert pokedex entries and typing back to tuple format for randomizer
def convert_to_tuple(test):

    list = test.split("', ")

    for i in range(0, len(list)):
        if list[i].startswith("["):
            list[i].replace("[",'')
        if test.endswith("]"):
            list[i].replace("]",'')
        list[i] += "'"
    return list

##connection to DB
connection_string = ''


client = MongoClient(connection_string)
Pokemon_list = client.db["PokemonDB"]

## Convert CSV back to dictionary
pkmdb_read = pd.read_csv("Pokedle_2_Revised.csv")
pokemon_list = pkmdb_read.to_dict("split")
pokemon_list = dict(zip(pokemon_list["index"], pokemon_list["data"]))

##Take dictionary and format to upload to cloud DB

# for i in range(0, len(pokemon_list[0])):
#     pokemon = {
#     '_id' : i,
#     'p_id' : pokemon_list[0][i],
#     'p_avatar': pokemon_list[1][i],
#     'p_nme': pokemon_list[2][i],
#     'p_types': pokemon_list[3][i],
#     'p_ability': pokemon_list[4][i],
#     'p_height': pokemon_list[5][i],
#     'p_weight': pokemon_list[6][i],
#     'p_location': pokemon_list[7][i],
#     'p_evostage': pokemon_list[8][i],
#     'p_dex_entries': pokemon_list[9][i]
#     }
#     pokedex = Pokemon_list.insert_one(pokemon)

#   
cursor = Pokemon_list.find({"p_nme": "Absol"}) 
for record in cursor:
    print(record)



