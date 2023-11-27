import csv
import random
import math
import tkinter as tk
from textviewer import TextViewer


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
        return random.random() < 1/16

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
        text = f"\n{move_text}{critical_text}{effectiveness_text} and deals {damage} damage"
        root = tk.Tk()
        text_viewer = TextViewer(root)
        text_viewer.display_text(text)
        target_pokemon.receive_damage(damage, text_viewer, root)

    def receive_damage(self, damage, text_viewer, root):
        self.real_stats['hp'] = max(0, self.real_stats['hp'] - damage)
        # print(f"{self.name} now has {self.real_stats['hp']} HP.")
        text = f"{self.name} now has {self.real_stats['hp']} HP."
        text_viewer.display_text(text)
        root.mainloop()
        return self.real_stats['hp'] == 0