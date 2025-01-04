from main import Player, Enemy  # Importa as classes definidas em main.py
import random

# Configuração da tela
WIDTH = 800
HEIGHT = 600

# Animações do jogador
player_animations = {
    "stand": ["player/player_stand"],
    "walk": ["player/player_walk_1", "player/player_walk_2"]
}

# Animações dos inimigos
enemy_animations = {
    "stand": ["enemy/enemy_stand"],
    "walk": ["enemy/enemy_walk_1", "enemy/enemy_walk_2"]
}

# Criação do jogador e inimigos
player = Player(player_animations, "stand", (400, 300))
enemies = [
    Enemy(enemy_animations, "stand", (random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    for _ in range(3)
]

def draw():
    """
    Desenha todos os elementos na tela.
    """
    screen.fill((0, 0, 0))
    player.draw()
    for enemy in enemies:
        enemy.draw()

def update():
    """
    Atualiza os estados do jogo.
    """
    player.handle_input(keyboard)
    for enemy in enemies:
        enemy.follow(player.actor.pos)
    player.update_animation()
    for enemy in enemies:
        enemy.update_animation()
