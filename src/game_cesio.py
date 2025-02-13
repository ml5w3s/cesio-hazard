import time
import random
import pgzrun
from pgzero.actor import Actor

# Configurações da tela
WIDTH = 800
HEIGHT = 600

# Som
sound_enabled = True
if sound_enabled:
    sounds.kalimba_game.play()

# Estados do jogo
game_state = "intro"  # intro, menu, countdown, playing, exit
menu_options = ["Começar o jogo", "Música e sons: Ligado", "Sair"]
countdown = 3

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

# Elementos do jogo
player = None
door = None
obstacles = []
enemies = []
player_health = 1000
current_room = 1
game_over = False
game_won = False

# Atores e recursos da intro
capa = Actor("capa", (WIDTH // 2, HEIGHT // 2))
capa_desfocada = Actor("capa_desfocada", (WIDTH // 2, HEIGHT // 2))
em_breve = Actor("em_breve", (WIDTH // 2, HEIGHT // 2))

# Função para desenhar na tela
def draw():
    screen.clear()
    if game_state == "intro":
        capa.draw()
    elif game_state == "menu":
        capa_desfocada.draw()
        draw_menu()
    elif game_state == "countdown":
        screen.fill("black")
        screen.draw.text(f"{countdown}", center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="white")
    elif game_state == "playing":
        draw_game()
    elif game_state == "exit":
        em_breve.draw()

# Função para desenhar o menu
def draw_menu():
    screen.draw.text("MENU", center=(WIDTH // 2, 100), fontsize=80, color="green")
    for i, option in enumerate(menu_options):
        screen.draw.text(option, center=(WIDTH // 2, 300 + i * 50), fontsize=60, color="black")

# Função para desenhar o jogo principal
def draw_game():
    global player_health, current_room

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

# Função para atualizar a lógica do jogo
def update():
    global game_state, countdown

    if game_state == "countdown":
        time.sleep(1)
        countdown -= 1
        if countdown <= 0:
            start_game()

    elif game_state == "playing":
        update_game()

    elif game_state == "exit":
        em_breve.draw()
        time.sleep(2)
        exit()

# Função para tratar cliques do mouse
def on_mouse_down(pos):
    global game_state, sound_enabled

    if game_state == "intro":
        # Qualquer clique na tela move para o menu
        game_state = "menu"
    elif game_state == "menu":
        # Verifica qual opção do menu foi clicada
        for i, option in enumerate(menu_options):
            option_rect = Rect((WIDTH // 2 - 200, 300 + i * 50 - 20), (400, 40))
            if option_rect.collidepoint(pos):
                if i == 0:  # Começar o jogo
                    game_state = "countdown"
                elif i == 1:  # Alternar som
                    sound_enabled = not sound_enabled
                    menu_options[1] = "Música e sons: Ligado" if sound_enabled else "Música e sons: Desligado"
                    if sound_enabled:
                        sounds.kalimba_game.play()
                    else:
                        sounds.kalimba_game.stop()
                elif i == 2:  # Sair
                    game_state = "exit"

# Função para inicializar o jogo principal
def start_game():
    global player, door, obstacles, enemies, player_health, game_over, game_won, game_state

    player = Actor(player_sprites["stand"][0], (WIDTH // 2, HEIGHT // 2))
    door = Actor("door", (WIDTH - 50, HEIGHT // 2))
    obstacles = [
        Actor("obstacle", (200, 150)),
        Actor("obstacle", (400, 400)),
        Actor("obstacle", (600, 200))
    ]
    enemies = [
        Actor(enemy_sprites["stand"][0], (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)))
        for _ in range(3)
    ]
    game_over = False
    game_won = False
    game_state = "playing"

# Função para atualizar o jogo principal
def update_game():
    global player_health, current_room, game_over, game_won, frame_index, last_frame_time

    if game_over or game_won:
        return

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

    if moving:
        player.image = player_sprites["walk"][frame_index]
    else:
        player.image = player_sprites["stand"][frame_index]

    player.x += dx
    player.y += dy

    # Colisão com obstáculos
    for obstacle in obstacles:
        if player.colliderect(obstacle):
            if sound_enabled:
                sounds.ops.play()
            player.x -= dx
            player.y -= dy

    # Colisão com inimigos
    for enemy in enemies:
        if player.colliderect(enemy):
            if sound_enabled:
                sounds.eep.play()
            player_health -= 10

        # Movimento dos inimigos em direção ao jogador
        if player.x > enemy.x:
            enemy.x += 2
            enemy.image = enemy_sprites["walk"][frame_index]
        elif player.x < enemy.x:
            enemy.x -= 2
            enemy.image = enemy_sprites["walk"][frame_index]
        if player.y > enemy.y:
            enemy.y += 2
            enemy.image = enemy_sprites["walk"][frame_index]
        elif player.y < enemy.y:
            enemy.y -= 2
            enemy.image = enemy_sprites["walk"][frame_index]

    # Verificar vitória ou derrota
    if player_health <= 0:
        game_over = True
    elif player.colliderect(door):
        if sound_enabled:
            sounds.go.play()
        current_room += 1
        if current_room > 15:
            game_won = True
        else:
            start_game()

# Ligar o jogo
pgzrun.go()
