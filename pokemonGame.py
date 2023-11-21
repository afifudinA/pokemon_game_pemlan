import csv
import random
from battle import Battle
from pokemon import Pokemon

class Entity:
    def __init__(self, name, all_pokemon):
        self.name = name
        self.my_pokemon = random.sample(all_pokemon, 1)
        self.active_pokemon = None

    def switch_pokemon(self, enemy=False):
        if enemy:
            self.active_pokemon = random.choice(self.my_pokemon)
            return
        print(f"{self.name}, choose a Pokémon to switch to:")
        for i, pokemon in enumerate(self.my_pokemon, 1):
            print(f"{i}. {pokemon.name}")
        pokemon_choice = int(input("Enter the number of your chosen Pokémon: "))
        self.active_pokemon = self.my_pokemon[pokemon_choice - 1]
        print(f"{self.name} switched to {self.active_pokemon.name}.")

    def get_active_pokemon_speed(self):
        return self.active_pokemon.real_stats['speed']

    def get_active_pokemon(self):
        return self.active_pokemon

    def choose_move_or_switch(self):
        print(f"{self.name}'s turn:")
        # Default behavior: choose a random move
        move_name = random.choice(list(self.active_pokemon.move_pool.keys()))
        return self.active_pokemon.move_pool[move_name], move_name


class Player(Entity):
    def choose_move_or_switch(self):
        print(f"{self.name}'s turn:")
        print("1. Attack")
        print("2. Switch Pokémon")
        choice = input("Enter the number of your chosen action: ")

        if choice == '1':
            return self.choose_attack_move()
        elif choice == '2':
            self.switch_pokemon()
            return None, None
        else:
            print("Invalid choice. Defaulting to Attack.")
            return self.choose_attack_move()

    def choose_attack_move(self):
        print("Choose your Move:")
        for i, move_name in enumerate(self.active_pokemon.move_pool.keys(), 1):
            print(f"{i}. {move_name}")
        move_choice = int(input("Enter the number of your chosen Move: "))
        move_name = list(self.active_pokemon.move_pool.keys())[move_choice - 1]
        return self.active_pokemon.move_pool[move_name], move_name


class Enemy(Entity):
    pass  # No need to override, it will use the default behavior


def load_all_pokemon():
    pokemon_list = []
    with open('pokemon_data.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for index, row in enumerate(reader, start=1):
            name, level, types_str, stats_str, move_pool_str = row
            Types = eval(types_str)
            stats = eval(stats_str)
            move_pool = eval(move_pool_str)
            pokemon_instance = Pokemon(name, level, Types, stats, move_pool, index)
            pokemon_list.append(pokemon_instance)
    return pokemon_list


def choose_moves(all_pokemon):
    for pokemon in all_pokemon:
        move_pool_keys = list(pokemon.move_pool.keys())

        if len(move_pool_keys) >= 4:
            selected_moves = [move for move in random.sample(move_pool_keys, 4) if pokemon.move_pool[move].power != 'None']
            pokemon.move_pool = {move: pokemon.move_pool[move] for move in selected_moves}
        else:
            print(f"Removing {pokemon.name} because it has less than four moves.")
            all_pokemon.remove(pokemon)


def main():
    all_pokemon = load_all_pokemon()
    choose_moves(all_pokemon)
    player = Player("Udin", all_pokemon)
    enemy = Enemy("Justin", all_pokemon)
    battle = Battle(player, enemy)
    battle.start_battle()


if __name__ == '__main__':
    main()
