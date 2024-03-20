## Imports
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


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
for pokemon in pokemon_rows[6:7]:
    pokemon_data = pokemon.find_all("td")
##POKEID
    id = pokemon_data[0]['data-sort-value']
    print(id)
##Images
    avatar = pokemon_data[0].find_all("img")[0]['src']
    print(avatar)
##name
    name = pokemon_data[1].find_all("a")[0].getText()
    if pokemon_data[1].find_all("small"):
        name  = pokemon_data[1].find_all("small")[0].getText()
    print(name)
## types
    types = []
    for pokemon_type in pokemon_data[2].find_all("a"):
        types.append (pokemon_type.getText())
    print(types)
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
    print(height+"\n" +weight + "\n")
        
##Get dex info
    dex_entries = []
    count  = 2
    pokemon_dexinf = entry_soup.find_all("main")[0].find_all("div", {"class": "resp-scroll"})[2].find_all ("td", {"class": "cell-med-text"})


    while len(dex_entries) == 1 or len(dex_entries) == 0:
        try:
            if count > 0:
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
    
    for x in range(len(dex_entries)):
        print(dex_entries[x])
    

   

##Scraper