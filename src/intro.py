from time import sleep
from pgzero.actor import Actor
from pgzero.keyboard import keys
import pgzrun

# Configurações da tela
WIDTH = 800
HEIGHT = 600

# Estados do jogo
game_state = "intro"  # intro, menu, countdown, playing
sound_enabled = True

# Atores e recursos
capa = Actor("capa", (WIDTH // 2, HEIGHT // 2))
capa_desfocada = Actor("capa_desfocada", (WIDTH // 2, HEIGHT // 2))
em_breve = Actor("em_breve", (WIDTH // 2, HEIGHT // 2))
menu_options = ["Começar o jogo", "Música: Ligada", "Saída"]
menu_selected = 0
countdown = 3

# Desenhar na tela
def draw():
    screen.clear()
    if game_state == "intro":
        capa.draw()
    elif game_state == "menu":
        capa_desfocada.draw()
        draw_menu()
    elif game_state == "countdown":
        screen.fill("black")
        screen.draw.text(f"{countdown}...", center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="white")
    elif game_state == "exit":
        em_breve.draw()

# Desenhar o menu
def draw_menu():
    screen.draw.text("CESIO HAZARD", center=(WIDTH // 2, 100), fontsize=60, color="lime")
    for i, option in enumerate(menu_options):
        color = "white" if i == menu_selected else "gray"
        screen.draw.text(option, center=(WIDTH // 2, 200 + i * 50), fontsize=40, color=color)

# Atualizar lógica do jogo
def update():
    global game_state, menu_selected, sound_enabled, countdown

    if game_state == "intro" and keyboard.space:
        game_state = "menu"

    elif game_state == "menu":
        if keyboard.up and menu_selected > 0:
            menu_selected -= 1
        elif keyboard.down and menu_selected < len(menu_options) - 1:
            menu_selected += 1

        if keyboard.RETURN or keyboard.SPACE:
            if menu_selected == 0:  # Começar o jogo
                game_state = "countdown"
            elif menu_selected == 1:  # Música Ligada/Desligada
                sound_enabled = not sound_enabled
                menu_options[1] = "Música: Ligada" if sound_enabled else "Música: Desligada"
            elif menu_selected == 2:  # Saída
                game_state = "exit"

    elif game_state == "countdown":
        sleep(1)
        countdown -= 1
        if countdown <= 0:
            game_state = "playing"  # Você pode trocar aqui para o estado de jogo principal.

    elif game_state == "exit":
        sleep(2)
        exit()

# Ligar o jogo
pgzrun.go()
