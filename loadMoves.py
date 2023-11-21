import requests
import csv

def get_move_data(name):
    url = f'https://pokeapi.co/api/v2/move/{name}/'
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        return None


def load_move_detail():
    pokemon_list = []
    with open('pokemon_data.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for index, row in enumerate(reader,start=1):
            name, level, types_str, stats_str, move_pool_str = row
            
            move_pool = eval(move_pool_str)
            
            pokemon_moves = move_pool
            
            for move in pokemon_moves:
                move_detail = get_move_data(move)
                print(move, " is ",move_detail['damage_class']['name'])
            break
    return pokemon_list

def main():
    load_move_detail()

if __name__ == '__main__':
    main()