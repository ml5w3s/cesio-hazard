from time import sleep
from pgzero.actor import Actor
import pgzrun
import subprocess

# Configurações da tela
WIDTH = 800
HEIGHT = 600

# Som da introdução
sounds.kalimba_game.play()

# Estados do jogo
game_state = "intro"  # intro, menu, countdown, playing, exit
sound_enabled = True

# Atores e recursos
capa = Actor("capa", (WIDTH // 2, HEIGHT // 2))
capa_desfocada = Actor("capa_desfocada", (WIDTH // 2, HEIGHT // 2))
em_breve = Actor("em_breve", (WIDTH // 2, HEIGHT // 2))
menu_options = ["Começar o jogo", "Música e sons", "Sair"]
menu_selected = 0
countdown = 3

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
    elif game_state == "exit":
        em_breve.draw()

# Função para desenhar o menu
def draw_menu():
    screen.draw.text("MENU", center=(WIDTH // 2, 100), fontsize=80, color="green")
    for i, option in enumerate(menu_options):
        color = "black" if i == menu_selected else "gray"
        screen.draw.text(option, center=(WIDTH // 2, 300 + i * 50), fontsize=60, color=color)

# Função para atualizar a lógica do jogo
def update():
    global game_state, menu_selected, countdown

    if game_state == "intro":
        # Aguarda evento de clique ou tecla espaço para mudar para o menu
        if keyboard.space:
            game_state = "menu"

    elif game_state == "menu":
        # Navegação no menu com teclado
        if keyboard.up and menu_selected > 0:
            menu_selected -= 1
        elif keyboard.down and menu_selected < len(menu_options) - 1:
            menu_selected += 1

        # Seleção de opções do menu
        if keyboard.RETURN or keyboard.SPACE:
            if menu_selected == 0:  # Começar o jogo
                game_state = "countdown"
            elif menu_selected == 1:  # Sair
                game_state = "exit"

    elif game_state == "countdown":
        sleep(1)
        countdown -= 1
        if countdown <= 0:
            # Troque para o seu jogo principal aqui
            subprocess.run(["python3", "game.py"])
            exit()

    elif game_state == "exit":
        sleep(2)
        exit()

# Função para tratar cliques do mouse
def on_mouse_down(pos):
    global game_state
    if game_state == "intro":
        game_state = "menu"

# Ligar o jogo
pgzrun.go()
