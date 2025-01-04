import random
from pgzero.actor import Actor

# Configuração da tela
WIDTH = 800
HEIGHT = 600

# Jogador
player = Actor("player/player_stand", (WIDTH // 2, HEIGHT // 2))

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
    Actor("enemy/enemy_stand", (random.randint(0, WIDTH), random.randint(0, HEIGHT)))
    for _ in range(3)
]

def generate_new_room():
    """
    Gera uma nova sala com obstáculos e inimigos em posições aleatórias.
    """
    global enemies, obstacles

    # Reposiciona o jogador na entrada
    player.pos = (50, HEIGHT // 2)

    # Reposiciona a porta
    door.pos = (WIDTH - 50, random.randint(100, HEIGHT - 100))

    # Gera novos inimigos
    enemies = [
        Actor("enemy/enemy_stand", (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)))
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
    screen.fill((0, 0, 0))  # Fundo preto
    player.draw()
    door.draw()
    for enemy in enemies:
        enemy.draw()
    for obstacle in obstacles:
        obstacle.draw()

def update():
    """
    Atualiza os estados do jogo.
    """
    # Movimento do jogador
    dx = dy = 0
    if keyboard.left:
        dx -= 5
    if keyboard.right:
        dx += 5
    if keyboard.up:
        dy -= 5
    if keyboard.down:
        dy += 5

    # Atualiza a posição do jogador
    player.x += dx
    player.y += dy

    # Verifica colisão com obstáculos
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            sounds.ops.play() # Toca som ao colidir com obstáculo
            player.x -= dx  # Reverte o movimento
            player.y -= dy  # Reverte o movimento

    # Verifica colisão com inimigos
    for enemy in enemies:
        if player.colliderect(enemy):
            sounds.eep.play()  # Toca o som ao colidir com enemies
            print("Você tomou dano!")

    # Verifica colisão com a porta
    if player.colliderect(door):
        print("Mudando para uma nova sala!")
        sounds.go.play() # Toca o som ao colidir com porta
        generate_new_room()

    # Movimentação dos inimigos
    for enemy in enemies:
        if player.x > enemy.x:
            enemy.x += 2
        if player.x < enemy.x:
            enemy.x -= 2
        if player.y > enemy.y:
            enemy.y += 2
        if player.y < enemy.y:
            enemy.y -= 2
