import csv
import random
import math
import tkinter as tk

class TextViewer:
    def __init__(self, master):
        self.master = master
        self.text_widget = tk.Text(master, height=10, width=40)
        self.text_widget.pack()
        button_close = tk.Button(self.master, text="Close",  command=self.close_viewer)
        button_close.pack(side=tk.BOTTOM, pady=5)
        self.selected_choice = None  # Attribute to store the selected choice

    def display_text(self, text):
        current_text = self.text_widget.get("1.0", tk.END)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, current_text + text + "\n")
        

    def close_viewer(self):
        self.master.destroy()

    def display_choice(self, choices):
        center_frame = tk.Frame(self.master)
        center_frame.pack()

        for choice in choices:
            button_choice = tk.Button(center_frame, text=choice, command=lambda c=choice: self.on_choice_selected(c))
            button_choice.pack(side=tk.LEFT, padx=10)
        
            
    def on_choice_selected(self, choice):
        self.selected_choice = choice
        self.display_text(f"Selected choice: {choice}")
        self.master.destroy()
    
    


class Move:
    def __init__(self, name, power, accuracy, move_type):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.type = move_type

class Pokemon:
    def __init__(self, name, level, poke_type, stats, move_pool, index):
        self.name = name
        self.level = level
        self.type = poke_type
        self.real_stats = self.calculate_real_stat(stats)
        self.move_pool = {move_name: Move(move_name, move['power'], move['accuracy'], move['type']) for move_name, move in move_pool.items()}

    def calculate_real_stat(self, stats):
        real_stats = {}
        stat_names = ['hp', 'attack', 'defense', 'special attack', 'special defense', 'speed']

        for stat in stat_names:
            base_stat = int(stats.get(stat, 0))
            real_stats[stat] = math.floor(0.01 * (2 * base_stat + 31 + math.floor(0.25 * 255)) * int(self.level)) + 5

        real_stats['hp'] += int(self.level) + 5
        return real_stats

    def is_critical(self):
        return random.random() < 0.0625

    def is_stab(self, move_type):
        return move_type == self.type

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

    def calculate_damage(self, move, target_pokemon):
        accuracy = float(move.accuracy) if move.accuracy is not None else 100.0
        if random.random() > accuracy / 100.0:
            return 0, False, " but the attack missed!"

        critical_multiplier = 2.0 if self.is_critical() else 1.0
        stab_multiplier = 1.5 if self.is_stab(move.type) else 1.0
        effectiveness_multiplier = self.is_super_effective(move.type, target_pokemon.type)

        is_critical = critical_multiplier > 1.0

        if effectiveness_multiplier == 2.0:
            effectiveness_text = " it's Super effective!"
        elif effectiveness_multiplier == 0.5:
            effectiveness_text = " it's not very effective!"
        elif effectiveness_multiplier == 0.0:
            effectiveness_text = " it's not effective at all!"  # or any other message for immune
        else:
            effectiveness_text = ""

        base_damage = int(move.power) if move.power is not None else 0
        attack_stat = int(self.real_stats['attack'])
        defense_stat = int(target_pokemon.real_stats['defense'])
        damage = ((2 * int(self.level) / 5 + 2) * base_damage * attack_stat / defense_stat) / 50 + 2
        damage *= critical_multiplier * int(stab_multiplier) * effectiveness_multiplier

        return int(damage), is_critical, effectiveness_text

    def attack(self, move, target_pokemon):
        damage, is_critical, effectiveness_text = self.calculate_damage(move, target_pokemon)
        move_text = f"{self.name} used {move.name}"
        critical_text = " it's Critical hit!" if is_critical else ""
        print(f"\n{move_text}{critical_text}{effectiveness_text}")
        target_pokemon.receive_damage(damage)

    def receive_damage(self, damage):
        self.real_stats['hp'] = max(0, self.real_stats['hp'] - damage)
        print(f"{self.name} now has {self.real_stats['hp']} HP.")
        return self.real_stats['hp'] == 0

class Entity:
    def __init__(self, name, all_pokemon):
        self.name = name
        self.my_pokemon = random.sample(all_pokemon, 2)
        self.active_pokemon = None

    def switch_pokemon(self, enemy=False):
        if enemy:
            self.active_pokemon = random.choice(self.my_pokemon)
            return
        if len(self.my_pokemon) == 1:
            self.active_pokemon = self.my_pokemon[0]
            return
        text = self.name+ " choose a Pokémon to switch to:"
        root = tk.Tk()
        text_viewer = TextViewer(root)
        text_viewer.display_text(text)
        text = "" 
        for i, pokemon in enumerate(self.my_pokemon, 1):
            text += str(i) + ". " + pokemon.name + "\n"
            print(f"{i}. {pokemon.name}")
        num_choices = len(self.my_pokemon)
        text_viewer.display_text(text)    
        text_viewer.display_choice(list(map(str, range(1, num_choices + 1))))
        root.mainloop()
        pokemon_choice = int(text_viewer.selected_choice)
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
        text = self.name + "'s turn: \n1. Attack\n2. Switch Pokemon"
        root = tk.Tk()
        text_viewer = TextViewer(root)
        text_viewer.display_text(text)
        text_viewer.display_choice(['1', '2'])
        root.mainloop()
        choice = text_viewer.selected_choice
        if choice == '1':
            return self.choose_attack_move()
        elif choice == '2':
            self.switch_pokemon()
            return None, None
        else:
            print("Invalid choice. Defaulting to Attack.")
            return self.choose_attack_move()

    def choose_attack_move(self):
        root = tk.Tk()
        text_viewer = TextViewer(root)
        text_viewer.display_text("Choose Your Move: ")
        move_text = ""
        for i, move_name in enumerate(self.active_pokemon.move_pool.keys(), 1):
            move_text += str(i) + ". " + move_name + "\n"
        text_viewer.display_text(move_text)
        text_viewer.display_choice(['1','2','3','4'])        
        root.mainloop()
        move_choice = int(text_viewer.selected_choice)
        move_name = list(self.active_pokemon.move_pool.keys())[move_choice - 1]
        return self.active_pokemon.move_pool[move_name], move_name

class Enemy(Entity):
    pass  # No need to override, it will use the default behavior

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start_battle(self):
        self.player.switch_pokemon()
        self.enemy.active_pokemon = random.choice(self.enemy.my_pokemon)

        while True:
            player_moves_first = self.player.get_active_pokemon_speed() > self.enemy.get_active_pokemon_speed() or (
                    self.player.get_active_pokemon_speed() == self.enemy.get_active_pokemon_speed() and random.choice([True, False])
            )

            player_move, move_name = self.player.choose_move_or_switch()

            if player_moves_first:
                self.player_turn(player_move)
            else:
                self.enemy_turn(player_move)

    def player_turn(self, player_move):
        if player_move is not None:
            self.execute_move(self.player, player_move, self.enemy)

        enemy_move_name = random.choice(list(self.enemy.get_active_pokemon().move_pool.keys()))
        enemy_move = self.enemy.get_active_pokemon().move_pool[enemy_move_name]
        enemy_move.name = enemy_move_name
        self.execute_move(self.enemy, enemy_move, self.player)

    def enemy_turn(self, player_move):
        enemy_move_name = random.choice(list(self.enemy.get_active_pokemon().move_pool.keys()))
        enemy_move = self.enemy.get_active_pokemon().move_pool[enemy_move_name]
        enemy_move.name = enemy_move_name
        self.execute_move(self.enemy, enemy_move, self.player)

        if player_move is not None:
            self.execute_move(self.player, player_move, self.enemy)

    def execute_move(self, attacker, move, target):
        attacker.get_active_pokemon().attack(move, target.get_active_pokemon())
        if target.get_active_pokemon().real_stats['hp'] <= 0:
            self.handle_fainted_pokemon(target)

    def handle_fainted_pokemon(self, entity):
        print(f"{entity.name}'s {entity.get_active_pokemon().name} has fainted!")
        entity.my_pokemon.remove(entity.active_pokemon)
        if not entity.my_pokemon:
            print(f"{self.get_opponent(entity).name}'s Won!")
            exit()
        entity.switch_pokemon()

    def get_opponent(self, entity):
        return self.enemy if entity == self.player else self.player

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
            # print(f"Removing {pokemon.name} because it has less than four moves.")
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
