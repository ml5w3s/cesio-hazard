import random
import time
from pgzero.actor import Actor

# Configuração da tela
WIDTH = 800
HEIGHT = 600

# Som da introdução
sounds.kalimba_game.play()

# Variáveis de estado do jogo
player_health = 1000
current_room = 1
game_over = False
game_won = False

# Sprites e animações
player_sprites = {
    "stand": ["player/player_stand_1", "player/player_stand_2"],
    "walk": ["player/player_walk_1", "player/player_walk_2"]
}
enemy_sprites = {
    "stand": ["enemy/enemy_stand_1", "enemy/enemy_stand_2"],
    "walk": ["enemy/enemy_walk_1", "enemy/enemy_walk_2"]
}

# Controle de frames para animação
frame_index = 0
frame_time = 0.2  # Tempo entre os frames (em segundos)
last_frame_time = time.time()

# Jogador
player = Actor(player_sprites["stand"][0], (WIDTH // 2, HEIGHT // 2))

# Porta
door = Actor("door", (WIDTH - 50, HEIGHT // 2))

# Obstáculos
obstacles = [
    Actor("obstacle", (200, 150)),
    Actor("obstacle", (400, 400)),
    Actor("obstacle", (600, 200))
]

# Inimigos
enemies = [
    Actor(enemy_sprites["stand"][0], (random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    for _ in range(3)
]

def generate_new_room():
    """
    Gera uma nova sala com obstáculos e inimigos em posições aleatórias.
    """
    global enemies, obstacles, current_room

    # Atualiza o número da sala
    current_room += 1

    # Reposiciona o jogador na entrada
    player.pos = (50, HEIGHT // 2)

    # Reposiciona a porta
    door.pos = (WIDTH - 50, random.randint(100, HEIGHT - 100))

    # Gera novos inimigos
    enemies = [
        Actor(enemy_sprites["stand"][0], (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)))
        for _ in range(3)
    ]

    # Gera novos obstáculos
    obstacles = [
        Actor("obstacle", (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)))
        for _ in range(4)
    ]

def draw():
    """
    Desenha todos os elementos na tela.
    """
    if game_over:
        screen.fill((0, 0, 0))  # Fundo preto
        screen.draw.text("Você Perdeu!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="red")
        screen.draw.text(f"Sala alcançada: {current_room}", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")
        return

    if game_won:
        screen.fill((0, 45, 0))  # Fundo verde
        screen.draw.text("Você Venceu!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="green")
        screen.draw.text(f"Sala alcançada: {current_room}", center=(WIDTH // 2, HEIGHT // 2 + 50), fontsize=30, color="white")
        return

    # Desenha o jogo
    screen.fill((0, 0, 0))  # Fundo preto
    player.draw()
    door.draw()
    for enemy in enemies:
        enemy.draw()
    for obstacle in obstacles:
        obstacle.draw()

    # Informações do jogo
    screen.draw.text(f"Sala: {current_room}", (10, 10), fontsize=30, color="white")
    screen.draw.text(f"Saúde: {player_health}", (10, 50), fontsize=30, color="white")

def update():
    """
    Atualiza os estados do jogo.
    """
    global player_health, game_over, game_won, frame_index, last_frame_time

    if game_over or game_won:
        return

    # Controle da animação por tempo
    now = time.time()
    if now - last_frame_time > frame_time:
        last_frame_time = now
        frame_index = (frame_index + 1) % len(player_sprites["stand"])

    # Movimento do jogador
    dx = dy = 0
    moving = False
    if keyboard.left:
        dx -= 5
        moving = True
    if keyboard.right:
        dx += 5
        moving = True
    if keyboard.up:
        dy -= 5
        moving = True
    if keyboard.down:
        dy += 5
        moving = True

    # Alterna entre os sprites de acordo com o movimento
    if moving:
        player.image = player_sprites["walk"][frame_index]
    else:
        player.image = player_sprites["stand"][frame_index]

    # Atualiza a posição do jogador
    player.x += dx
    player.y += dy

    # Verifica colisão com obstáculos
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            sounds.ops.play()  # Toca o som ao colidir
            player.x -= dx  # Reverte o movimento
            player.y -= dy  # Reverte o movimento

    # Verifica colisão com inimigos
    for enemy in enemies:
        if player.colliderect(enemy):
            sounds.eep.play()  # Toca o som ao colidir
            player_health -= 10
            print(f"Você tomou dano! Saúde: {player_health}")

    # Verifica se o jogador perdeu
    if player_health <= 0:
        game_over = True
        print("Fim de jogo! Você perdeu!")
        return

    # Verifica colisão com a porta
    if player.colliderect(door):
        sounds.go.play()
        print("Mudando para uma nova sala!")
        generate_new_room()

    # Verifica se o jogador venceu
    if current_room > 15:
        game_won = True
        print("Parabéns! Você venceu o jogo!")

    # Movimentação dos inimigos
    for enemy in enemies:
        if player.x > enemy.x:
            enemy.x += 2
            enemy.image = enemy_sprites["walk"][frame_index]
        if player.x < enemy.x:
            enemy.x -= 2
            enemy.image = enemy_sprites["walk"][frame_index]
        if player.y > enemy.y:
            enemy.y += 2
            enemy.image = enemy_sprites["walk"][frame_index]
        if player.y < enemy.y:
            enemy.y -= 2
            enemy.image = enemy_sprites["walk"][frame_index]
