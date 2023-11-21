import requests
import csv

class Pokemon:
    def __init__(self, pokemon_data):
        self.name = pokemon_data['name']
        self.level = 50
        self.Type = self.get_pokemon_type(pokemon_data['types'])
        self.stats = self.get_pokemon_stats(pokemon_data['stats'])
        self.move_pool = self.get_pokemon_move_pool(pokemon_data["moves"], self.level)
        print(f"{self.name} Successfully created")

        
    def get_pokemon_stats(self, pokemon_stats):
        stats = {}
        for entry in pokemon_stats:
            stats [entry['stat']['name']] = entry['base_stat']
        return stats
        
    def get_pokemon_move_pool(self, pokemon_moves, level):
        move_pool = {}
        for entry in pokemon_moves:
            move_details = entry['version_group_details']
            move_name = entry['move']
            
            for details in move_details:
                if details['version_group']['name'] == "red-blue" and details['level_learned_at'] < level:
                    move_class = move_name['name']
                    move_atr = self.get_move_data(move_class)
                    move_class = move_atr['damage_class']['name']
                    
                    if move_class == 'physical' or move_class == 'special':
                        move_name_key = move_name['name']
                        
                        # Create a dictionary for each move inside move_pool
                        move_pool[move_name_key] = {
                            'accuracy': move_atr['accuracy'],
                            'power': move_atr['power'],
                            'pp': move_atr['pp'],
                            'priority': move_atr['priority'],
                            'damage_class': move_class,
                            'type' : move_atr['type']['name']
                        }

        return move_pool

        
    def get_pokemon_type(self, pokemon_types):
        types = []
        for entry in pokemon_types:
            type_name = entry['type']['name']
            types.append(type_name)
        return types
    
    def to_csv_row(self):
        return [self.name, self.level, self.Type, self.stats, self.move_pool]
    
    def get_move_data(self, name):
        url = f'https://pokeapi.co/api/v2/move/{name}/'
        response = requests.get(url)

        if response.status_code == 200:
            move_data = response.json()
            return move_data
        else:
            return None


def get_pokemon_data(identifier):
    url = f'https://pokeapi.co/api/v2/pokemon/{identifier}/'
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        return None
    
def write_to_csv(pokemon_list, filename='pokemon_data.csv'):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Level', 'Type', 'Stats', 'Move Pool'])
        for pokemon_instance in pokemon_list:
            writer.writerow(pokemon_instance.to_csv_row())

def main():
    pokemon_list = []
    for pokemon_id in range(1,152):
        pokemon_data = get_pokemon_data(pokemon_id)
        if pokemon_data:
            pokemon_instance = Pokemon(pokemon_data)
            pokemon_list.append(pokemon_instance)
            
    write_to_csv(pokemon_list)

if __name__ == "__main__":
    main()