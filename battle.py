import random

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
                self.enemy_turn(player_move)  # Fix here

    def player_turn(self,player_move):
        if player_move is not None:
            self.player.get_active_pokemon().attack(player_move, self.enemy.get_active_pokemon())
            if self.enemy.get_active_pokemon().real_stats['hp'] <= 0:
                print(f"{self.enemy.name}'s {self.enemy.get_active_pokemon().name} has fainted!")
                self.enemy.my_pokemon.remove(self.enemy.active_pokemon)
                if not self.enemy.my_pokemon:
                    print(f"{self.player.name}'s Won!")
                    exit()
                self.enemy.switch_pokemon(True)

            enemy_move_name = random.choice(list(self.enemy.get_active_pokemon().move_pool.keys()))
            enemy_move = self.enemy.get_active_pokemon().move_pool[enemy_move_name]
            enemy_move.name = enemy_move_name
            self.enemy.get_active_pokemon().attack(enemy_move, self.player.get_active_pokemon())

            if self.player.get_active_pokemon().real_stats['hp'] <= 0:
                print(f"{self.player.name}'s {self.player.get_active_pokemon().name} has fainted!")
                self.player.my_pokemon.remove(self.player.active_pokemon)
                if not self.player.my_pokemon:
                    print(f"{self.enemy.name}'s Won!")
                    exit()
                self.player.switch_pokemon()

    def enemy_turn(self, player_move):
        enemy_move_name = random.choice(list(self.enemy.get_active_pokemon().move_pool.keys()))
        enemy_move = self.enemy.get_active_pokemon().move_pool[enemy_move_name]
        enemy_move.name = enemy_move_name
        self.enemy.get_active_pokemon().attack(enemy_move, self.player.get_active_pokemon())

        if self.player.get_active_pokemon().real_stats['hp'] <= 0:
            print(f"{self.player.name}'s {self.player.get_active_pokemon().name} has fainted!")
            self.player.my_pokemon.remove(self.player.active_pokemon)
            if not self.player.my_pokemon:
                print(f"{self.enemy.name}'s Won!")
                exit()
            self.player.switch_pokemon()

        if player_move is not None:
            self.player.get_active_pokemon().attack(player_move, self.enemy.get_active_pokemon())
            if self.enemy.get_active_pokemon().real_stats['hp'] <= 0:
                print(f"{self.enemy.name}'s {self.enemy.get_active_pokemon().name} has fainted!")
                self.enemy.my_pokemon.remove(self.enemy.active_pokemon)
                if not self.enemy.my_pokemon:
                    print(f"{self.player.name}'s Won!")
                    exit()
                self.enemy.switch_pokemon(True)