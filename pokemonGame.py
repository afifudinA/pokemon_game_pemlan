import csv
import random
import math


class Pokemon:
    def __init__(self, name, level, poke_type, stats, move_pool, index):
        self.name = name
        self.level = level
        self.type = poke_type
        self.real_stats = self.calculate_real_stat(stats)
        self.move_pool = move_pool

    def is_critical(self):
        # Placeholder for critical hit logic
        return random.random() < 1/16 

    def is_super_effective(self, move_type, target_types):
        with open('type_relations.csv', newline='') as f:
            reader = csv.DictReader(f)
            for target_type in target_types:    
                for row in reader:
                    if row['Type'] == move_type:
                        effectiveness = 1.0  # Placeholder, you need to implement this based on your type chart
                        for key in ['Double Damage To', 'Half Damage To', 'No Damage To']:
                            if target_type in row[key]:
                                effectiveness *= 2.0 if 'Double' in key else 0.5 if 'Half' in key else 0.0
                return effectiveness
        return 1.0

    def is_stab(self, move_type):
        # Placeholder for Same Type Attack Bonus (STAB) logic
        return move_type == self.type

    def calculate_damage(self, move, target_pokemon):
        accuracy = float(move['accuracy']) if move['accuracy'] is not None else 100.0
        # Check if the attack lands based on accuracy
        if random.random() > accuracy / 100.0:
            return 0, False, " but the attack missed!"

        critical_multiplier = 2.0 if self.is_critical() else 1.0
        stab_multiplier = 1.5 if self.is_stab(move['type']) else 1.0
        effectiveness_multiplier = self.is_super_effective(move['type'], target_pokemon.type)
        
        is_critical = critical_multiplier > 1.0
        
        if effectiveness_multiplier == 2.0:
            effectiveness_text = " it's Super effective!"
        elif effectiveness_multiplier == 0.5:
            effectiveness_text = " it's not very effective!"
        elif effectiveness_multiplier == 0.0:
            effectiveness_text = " it's not effective at all!"  # or any other message for immune
        else:
            effectiveness_text = ""

        base_damage = int(move['power']) if move['power'] is not None else 0
        attack_stat = int(self.real_stats['attack'])
        defense_stat = int(target_pokemon.real_stats['defense'])
        damage = ((2 * int(self.level) / 5 + 2) * base_damage * attack_stat / defense_stat) / 50 + 2
        damage *= critical_multiplier * int(stab_multiplier) * effectiveness_multiplier

        return int(damage), is_critical, effectiveness_text


    def calculate_real_stat(self, stats):
        real_stats = {'hp': 0, 'attack': 0, 'defense': 0,'special attack' : 0, 'special paradise' : 0 ,  'speed': 0}
        real_stats['hp'] = math.floor(0.01 * (2 * int(stats['hp']) + 31 + math.floor(0.25 * 255)) * int(self.level)) + int(self.level) + 10
        real_stats['attack'] = math.floor(0.01 * (2 * int(stats['attack']) + 31 + math.floor(0.25 * 255)) * int(self.level)) + 5
        real_stats['defense'] = math.floor(0.01 * (2 * int(stats['defense']) + 31 + math.floor(0.25 * 255)) * int(self.level)) + 5
        real_stats['special attack'] = math.floor(0.01 * (2 * int(stats['special-attack']) + 31 + math.floor(0.25 * 255)) * int(self.level)) + 5
        real_stats['special defense'] = math.floor(0.01 * (2 * int(stats['special-defense']) + 31 + math.floor(0.25 * 255)) * int(self.level)) + 5
        return real_stats

    def attack(self, move, target_pokemon):
        damage, is_critical, effectiveness_text = self.calculate_damage(move, target_pokemon)
        
        # Text indicators
        move_text = f"{self.name} used {move['name']}"
        critical_text = " it's Critical hit!" if is_critical else ""

        print(f"\n{move_text}{critical_text}{effectiveness_text}")
        target_pokemon.receive_damage(damage)



    def switch(self, new_pokemon):
        print(f"{self.name} switched to {new_pokemon.name}.")
        return new_pokemon

    def receive_damage(self, damage):
        # Placeholder for receiving damage logic
        self.real_stats['hp'] -= damage
        if self.real_stats['hp'] < 0:
            self.real_stats['hp'] = 0
        print(f"{self.name} now has {self.real_stats['hp']} HP.")
        return self.real_stats['hp'] == 0



class Player:
    def __init__(self, name, all_pokemon):
        self.name = name
        self.my_pokemon = random.sample(all_pokemon, 3)
        self.active_pokemon = None
        

    def switch_pokemon(self, enemy = False):
        if enemy:
            self.active_pokemon = random.choice(self.my_pokemon)
            return
        print(f"{self.name}, choose a Pokémon to switch to:")
        for i, pokemon in enumerate(self.my_pokemon, 1):
            print(f"{i}. {pokemon.name}")
        pokemon_choice = int(input("Enter the number of your chosen Pokémon: "))
        self.active_pokemon = self.my_pokemon[pokemon_choice - 1]
        print(f"{self.name} switched to {self.active_pokemon.name}.")
        
    def choose_move_or_switch(self):
        print(f"{self.name}'s turn:")
        print("1. Attack")
        print("2. Switch Pokémon")
        choice = input("Enter the number of your chosen action: ")
        
        if choice == '1':
            # Choose a Move
            print("Choose your Move:")
            for i, move_name in enumerate(self.active_pokemon.move_pool.keys(), 1):
                print(f"{i}. {move_name}")
            move_choice = int(input("Enter the number of your chosen Move: "))
            move_name = list(self.active_pokemon.move_pool.keys())[move_choice - 1]
            self.active_pokemon.move_pool[move_name]['name'] = move_name
            return self.active_pokemon.move_pool[move_name], move_name
        elif choice == '2':
            self.switch_pokemon()
            return None, None
        else:
            print("Invalid choice. Defaulting to Attack.")
            # Default to attacking if an invalid choice is made
            print("Choose your Move:")
            for i, move_name in enumerate(self.active_pokemon.move_pool.keys(), 1):
                print(f"{i}. {move_name}")
            move_choice = int(input("Enter the number of your chosen Move: "))
            move_name = list(self.active_pokemon.move_pool.keys())[move_choice - 1]
            self.active_pokemon.move_pool[move_name]['name'] = move_name
            return self.active_pokemon.move_pool[move_name], move_name

    def get_active_pokemon_speed(self):
        return self.active_pokemon.real_stats['speed']

    def get_active_pokemon(self):
        # print(self.active_pokemon)
        return self.active_pokemon


def load_all_pokemon():
    pokemon_list = []
    with open('pokemon_data.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        for index, row in enumerate(reader,start=1):
            name, level, types_str, stats_str, move_pool_str = row
            
            Types = eval(types_str)
            stats = eval(stats_str)
            move_pool = eval(move_pool_str)
            
            pokemon_instance = Pokemon(name, level, Types, stats, move_pool, index)
            pokemon_list.append(pokemon_instance)
            
    return pokemon_list

def choose_move(all_pokemon):
    for pokemon in all_pokemon:
        move_pool_keys = list(pokemon.move_pool.keys())

        if len(move_pool_keys) >= 4:
            selected_moves = [move for move in random.sample(move_pool_keys, 4) if pokemon.move_pool[move]['power'] != 'None']
            pokemon.move_pool = {move: pokemon.move_pool[move] for move in selected_moves}
            # print(f"Selected moves for {pokemon.name}: {pokemon.move_pool}")
        else:
            print(f"Removing {pokemon.name} because it has less than four moves.")
            all_pokemon.remove(pokemon)
            
def main():
    all_pokemon = load_all_pokemon()
    choose_move(all_pokemon)
    player = Player("Udin", all_pokemon)
    enemy = Player("Justin", all_pokemon)
    player.switch_pokemon()  # Player chooses the active Pokémon
    enemy.active_pokemon = random.choice(enemy.my_pokemon)
    while True:
        # Determine which player moves first based on the speed of their active Pokémon
        if player.get_active_pokemon_speed() > enemy.get_active_pokemon_speed():
            player_moves_first = True
        elif player.get_active_pokemon_speed() < enemy.get_active_pokemon_speed():
            player_moves_first = False
        else:
            # If the speeds are equal, randomly determine who moves first
            player_moves_first = random.choice([True, False])
        
        player_move, move_name = player.choose_move_or_switch()
        # Player's turn
        if player_moves_first:
            if player_move is not None:
                player.get_active_pokemon().attack(player_move, enemy.get_active_pokemon())

                # Check if the enemy's Pokémon has fainted
                if enemy.get_active_pokemon().real_stats['hp'] <= 0:
                    print(f"{enemy.name}'s {enemy.get_active_pokemon().name} has fainted!")
                    enemy.my_pokemon.remove(enemy.active_pokemon)
                    if not enemy.my_pokemon:
                        print(f"{player.name}'s Won!")
                        break  # End the battle if the enemy's Pokémon has fainted
                    enemy.switch_pokemon(True)

                enemy_move_name = random.choice(list(enemy.get_active_pokemon().move_pool.keys()))
                enemy_move = enemy.get_active_pokemon().move_pool[enemy_move_name]
                enemy_move['name'] = enemy_move_name
                enemy.get_active_pokemon().attack(enemy_move, player.get_active_pokemon())

                # Check if the player's Pokémon has fainted
                if player.get_active_pokemon().real_stats['hp'] <= 0:
                    print(f"{player.name}'s {player.get_active_pokemon().name} has fainted!")
                    player.my_pokemon.remove(player.active_pokemon)
                    if not player.my_pokemon:
                        print(f"{enemy.name}'s Won!")
                        break  # End the battle if the enemy's Pokémon has fainted
                    player.switch_pokemon()

        # Enemy's turn
        else:
            enemy_move_name = random.choice(list(enemy.get_active_pokemon().move_pool.keys()))
            enemy_move = enemy.get_active_pokemon().move_pool[enemy_move_name]
            enemy_move['name'] = enemy_move_name
            enemy.get_active_pokemon().attack(enemy_move, player.get_active_pokemon())

            # Check if the player's Pokémon has fainted
            if player.get_active_pokemon().real_stats['hp'] <= 0:
                print(f"{player.name}'s {player.get_active_pokemon().name} has fainted!")
                player.my_pokemon.remove(player.active_pokemon)
                if not player.my_pokemon:
                    print(f"{enemy.name}'s Won!")
                    break  # End the battle if the enemy's Pokémon has fainted
                player.switch_pokemon()
                
            if player_move is not None:
                player.get_active_pokemon().attack(player_move, enemy.get_active_pokemon())

                # Check if the enemy's Pokémon has fainted
                if enemy.get_active_pokemon().real_stats['hp'] <= 0:
                    print(f"{enemy.name}'s {enemy.get_active_pokemon().name} has fainted!")
                    enemy.my_pokemon.remove(enemy.active_pokemon)
                    if not enemy.my_pokemon:
                        print(f"{player.name}'s Won!")
                        break  # End the battle if the enemy's Pokémon has fainted
                    enemy.switch_pokemon(True)
                


if __name__ == '__main__':
    main()