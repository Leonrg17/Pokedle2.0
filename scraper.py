## Imports
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

pokemon_dict = {
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
def add_pokemon(id,avatar,name,types,height,weight,Location,evo_count,dex_entries,ability):
    pokemon_dict['p_id'].append(id)
    pokemon_dict['p_avatar'].append(avatar)
    pokemon_dict['p_nme'].append(name)
    pokemon_dict['p_types'].append(types)
    pokemon_dict['p_ability'].append(ability)
    pokemon_dict['p_height'].append(height)
    pokemon_dict['p_weight'].append(weight)
    pokemon_dict['p_location'].append(Location)
    pokemon_dict['p_evostage'].append(evo_count)
    pokemon_dict['p_dex_entries'].append(dex_entries)
 
def convert_to_tuple(test):

    list = test.split("', ")

    for i in range(0, len(list)):
        if list[i].startswith("["):
            list[i].replace("[",'')
        if test.endswith("]"):
            list[i].replace("]",'')
        list[i] += "'"
    return list

prev_evo = "teststring"
evo_count = 1

## URL
url = 'https://pokemondb.net/pokedex/all'

request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
)
page = urlopen(request)
page_contents_bytes = page.read()
page_html = page_contents_bytes.decode("utf-8")

soup = BeautifulSoup(page_html, "html.parser")

pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all('tbody')[0].find_all("tr")
for pokemon in pokemon_rows:
    pokemon_data = pokemon.find_all("td")
##POKEID
    id = pokemon_data[0]['data-sort-value']
##Images
    avatar = pokemon_data[0].find_all("img")[0]['src']
##name
    name = pokemon_data[1].find_all("a")[0].getText()
    if pokemon_data[1].find_all("small"):
        name  = pokemon_data[1].find_all("small")[0].getText()
    print(name)

## types
    types = []
    for pokemon_type in pokemon_data[2].find_all("a"):
        types.append (pokemon_type.getText())
 ##get details of pokemon   
    details_url = pokemon_data[1].find_all("a")[0]["href"]
    entry_url = f'https://pokemondb.net{details_url}'

    request = Request(
    entry_url,
    headers={'User-Agent': 'Mozilla/5.0'}
    )
    entry_page_url = urlopen(request).read().decode("utf-8")
    entry_soup = BeautifulSoup(entry_page_url, "html.parser")

    pokemon_entryinf = entry_soup.find("table", {"class" : "vitals-table"}).find_all("tbody")[0].find_all('tr')
    for pokemoninf in pokemon_entryinf:

        height = str(pokemon_entryinf[3].find_all('td')[0].getText())
        weight = str(pokemon_entryinf[4].find_all('td')[0].getText())

    ## Location first found
    Location = "Unknown"
    count = 0
    found = 0
    while count != 5 :
        while found != 5:
            try:
                pokemon_loc = entry_soup.find_all("main")[0].find_all("div",{"class": "grid-col span-md-12 span-lg-8"})[count].find_all("div",{"class":"resp-scroll"})[found].find_all("table",{"class":"vitals-table"})[found].find_all("td")[0].find_all("a")[0]
                Location = pokemon_loc.getText()

                pokemon_loc = entry_soup.find_all("main")[0].find_all("div",{"class": "grid-col span-md-12 span-lg-8"})[count].find_all("div",{"class":"resp-scroll"})[found].find_all("td")[0].find_all("small")[0]
                hstr = str(pokemon_loc.getText())
                if hstr.find("Evolve") != -1:
                    Location = "Unknown"
                    break
                elif hstr.find("Breed") != -1:
                    Location = "Unknown"
                    break        
            except IndexError:
                break
            found = found+1
        count = count+1
#get ability
    pokemon_ab = entry_soup.find_all("main")[0].find_all("div",{"class": "grid-col span-md-6 span-lg-4"})[0].find_all("span",{"class":"text-muted"})[0].find("a")
    ability = pokemon_ab.getText()

        
##Get dex info
    dex_entries = []
    count  = 0
    pokemon_dexinf = entry_soup.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[0].find_all ("td", {"class": "cell-med-text"})


    while len(dex_entries) == 1 or len(dex_entries) == 0:
        try:
            if count >= 0:
                for dex_entry in pokemon_dexinf:
                    dex_entries.append(dex_entry.getText())
                pokemon_dexinf = entry_soup.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[count].find_all ("td", {"class": "cell-med-text"})
            count = count+2
        except IndexError: 
            print ("no entries")
            break


##Give name ambiguity
    for x in range(len(dex_entries)):
        if (dex_entries[x].find(str(name)) != -1):
            dex_entries[x] = dex_entries[x].replace(str(name),'_______')
        elif (dex_entries[x].find(str(name).upper()) != -1):
            dex_entries[x] = dex_entries[x].replace(str(name).upper(),'_______')
        elif (dex_entries[x].find(str(name).lower()) != -1):
            dex_entries[x] = dex_entries[x].replace(str(name).lower(),'_______')
    

##get evloution info
 
   
    pokemon_evoinf = str(entry_soup.find_all("main")[0].find_all("div", {"class": "infocard-list-evo"}))
    if pokemon_evoinf.find(prev_evo) != -1:
        evo_count = evo_count + 1
        prev_evo = name
    else:
        evo_count = 1
        prev_evo = name
    
    add_pokemon(id,avatar,name,types,height,weight,Location,evo_count,dex_entries,ability)

##convert dictionary data to csv
df = pd.DataFrame.from_dict(pokemon_dict,orient='index')
df.to_csv("pokemon_data.csv")

##Convert CSV data into usable dictonary format

#test = pd.read_csv("pokemon_data.csv")
#d = test.to_dict("split")
#d = dict(zip(d["index"], d["data"]))

##Test case for converting pokedex entries back to tuples

#list = convert_to_tuple(str(d[8][3]))

#for i in range(0, len(list)):
#    print(list[i])


##Scraper