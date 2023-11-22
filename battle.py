import random
import tkinter as tk
from textviewer import TextViewer

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
        text = f"{entity.name}'s {entity.get_active_pokemon().name} has fainted!"
        root = tk.Tk()
        text_viewer = TextViewer(root)
        text_viewer.display_text(text)
        root.mainloop()
        entity.my_pokemon.remove(entity.active_pokemon)
        if not entity.my_pokemon:
            text = f"{entity.name} Out Of Pokemon!"
            root = tk.Tk()
            text_viewer = TextViewer(root)
            text_viewer.display_text(text)
            text = f"{self.get_opponent(entity).name}'s Won!"
            text_viewer.display_text(text)
            root.mainloop()
            exit()
        entity.switch_pokemon()

    def get_opponent(self, entity):
        return self.enemy if entity == self.player else self.player
