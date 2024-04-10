from pymongo import MongoClient

##connection to DB
connection_addr = 'localhost'
connection_port = 27017

##just for testing reminder
print("currently useing defaults: localhost on port 27017")

client = MongoClient(connection_addr, connection_port)

print("old: " + str(client.list_database_names()))

client.drop_database('PokemonDB')

print("new: " + str(client.list_database_names()))