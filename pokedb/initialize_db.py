from pymongo import MongoClient
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

##connection to DB
connection_addr = 'localhost'
connection_port = 27017

##just for testing reminder
print("currently useing defaults: localhost on port 27017")

client = MongoClient(connection_addr, connection_port)

#makes a database
Pokemon_list = client["PokemonDB"]

#makes a collection
PokemonC = Pokemon_list["PokemonC"]

## Convert CSV back to dictionary
pkmdb_read = pd.read_csv("Pokedle_2_Revised.csv")
pokemon_list = pkmdb_read.to_dict("split")
pokemon_list = dict(zip(pokemon_list["index"], pokemon_list["data"]))
# print(pokemon_list[1][1])
# print(len(pokemon_list[0]))

for i in range(1, len(pokemon_list[0])):
    pmon = {
        '_id' : i,
        'p_id' : pokemon_list[0][i],
        'p_avatar': pokemon_list[1][i],
        'p_nme': pokemon_list[2][i],
        'p_types': pokemon_list[3][i],
        'p_ability': pokemon_list[4][i],
        'p_height': pokemon_list[5][i],
        'p_weight': pokemon_list[6][i],
        'p_location': pokemon_list[7][i],
        'p_evostage': pokemon_list[8][i],
        'p_dex_entries': pokemon_list[9][i]
    }
    PokemonC.insert_one(pmon)

# for pokemon in PokemonC.find():
#     print(pokemon)