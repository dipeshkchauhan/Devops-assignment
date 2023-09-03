import requests

# Function to fetch JSON data from a URL
def get_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to get all starship names from the SWAPI API
def get_starship_names():
    starships = []
    url = "https://swapi.dev/api/starships/"
    
    while url:
        data = get_json_data(url)
        if data and "results" in data:
            starships.extend(data["results"])
            url = data.get("next")

    return starships

# Function to get all film names from the SWAPI API
def get_film_names():
    films = []
    url = "https://swapi.dev/api/films/"
    
    while url:
        data = get_json_data(url)
        if data and "results" in data:
            films.extend(data["results"])
            url = data.get("next")

    return films

# Function to filter starships by hyperdrive rating
def filter_starships_by_hyperdrive(starships, min_rating=1.0):
    return [starship["name"] for starship in starships if starship["hyperdrive_rating"] != "unknown" and float(starship["hyperdrive_rating"]) >= min_rating]

# Function to filter starships by crew size
def filter_starships_by_crew(starships, min_crew=3, max_crew=100):
    return [starship["name"] for starship in starships if starship["crew"].isdigit() and min_crew <= int(starship["crew"]) <= max_crew]

# Function to find starships that appeared in "Return of the Jedi"
def starships_in_return_of_jedi(films, starships):
    return_of_jedi_ships = []
    
    # Find the film "Return of the Jedi" from the list of films
    return_of_jedi_film = next((film for film in films if film["title"] == "Return of the Jedi"), None)
    
    if return_of_jedi_film:
        # Get the list of starship URLs from the film data
        starship_urls = return_of_jedi_film.get("starships", [])
        
        # Find starships that match the URLs in the film data
        return_of_jedi_ships = [starship["name"] for starship in starships if starship["url"] in starship_urls]

    return return_of_jedi_ships

if __name__ == '__main__':
    # Fetch starship and film data from SWAPI
    starships_list = get_starship_names()
    films_list = get_film_names()

    # Print starships that appeared in 'Return of the Jedi'
    print("Ships that appeared in 'Return of the Jedi':")
    return_of_jedi_ships = starships_in_return_of_jedi(films_list, starships_list)
    
    if return_of_jedi_ships:
        print(return_of_jedi_ships)
    else:
        print("No starships found for 'Return of the Jedi'.")

    # Print starships with hyperdrive rating >= 1.0
    print("Ships that have a hyperdrive rating >= 1.0:")
    hyperdrive_filtered = filter_starships_by_hyperdrive(starships_list, 1.0)
    print(hyperdrive_filtered)

    # Print starships with crews between 3 and 100
    print("Ships that have crews between 3 and 100:")
    crew_filtered = filter_starships_by_crew(starships_list, 3, 100)
    print(crew_filtered)
