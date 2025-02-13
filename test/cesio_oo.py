"""
Este é o módulo principal do jogo Cesio Hazard.

Ele define todas as classes e funções necessárias para gerenciar o jogo,
incluindo lógica de atualização, desenho na tela, detecção de colisões,
e a interface do menu.
"""

import time
import random
import pgzrun
from time import sleep
from pgzero.actor import Actor

# Configurações da tela
WIDTH = 800
HEIGHT = 600

# Carrega o plano de fundo
fundo = "fundo"  # "fundo.png" na pasta "images"

def play_sound_if_enabled(func):
    """
    Decorador para tocar sons apenas se o som estiver habilitado.
    """
    def wrapper(*args, **kwargs):
        if game.sound_enabled:  # Usa o estado global do jogo para verificar
            return func(*args, **kwargs)
    return wrapper

class Game:
    """
    Classe principal do jogo, gerencia o estado, a lógica e o fluxo do jogo.

    Atributos:
        state (str): Estado atual do jogo (intro, menu, countdown, playing, game_over, game_won).
        countdown (int): Contador regressivo antes de iniciar o jogo.
        current_room (int): Número da sala atual.
        player (Player): Objeto representando o jogador.
        enemies (list[Enemy]): Lista de inimigos na sala.
        obstacles (list[Obstacle]): Lista de obstáculos na sala.
        door (Door): Objeto representando a porta de saída da sala.
        menu_options (list[str]): Opções do menu principal.
        end_options (list[str]): Opções do menu de fim de jogo.
    """
    def __init__(self):
        """
        Inicializa o estado do jogo, incluindo os atores e os menus.
        """
        self.state = "intro"
        self.countdown = 3
        self.last_countdown_time = time.time()
        self.current_room = 1
        self.game_over = False
        self.game_won = False
        self.player = None
        self.enemies = []
        self.obstacles = []
        self.door = None

        # Intro e menu
        self.capa = Actor("capa", (WIDTH // 2, HEIGHT // 2))
        self.capa_desfocada = Actor("capa_desfocada", (WIDTH // 2, HEIGHT // 2))
        self.em_breve = Actor("em_breve", (WIDTH // 2, HEIGHT // 2))
        self.menu_options = ["Começar o jogo", "Música e sons: Ligado", "Sair"]
        self.end_options = ["Jogar Novamente", "Sair"]
        self.menu_selected = -1
        self.sound_enabled = True

        @play_sound_if_enabled
        def play_eep():
            sounds.ops.play()

        @play_sound_if_enabled
        def play_eep():
            sounds.go.play()

        @play_sound_if_enabled
        def play_eep():
            sounds.eep.play()

    def start_game(self):
        """
        Inicia uma nova partida, criando o jogador, os inimigos, os obstáculos e a porta.
        """
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.door = Door(WIDTH - 50, HEIGHT // 2)
        self.enemies = [Enemy(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) for _ in range(3)]
        self.obstacles = [
            Obstacle(200, 150),
            Obstacle(400, 400),
            Obstacle(600, 200)
        ]
        self.state = "playing"
        self.current_room = 1

    def update(self):
        """
        Atualiza o estado do jogo com base no estado atual.

        Controla a contagem regressiva, movimentação do jogador, e detecção de colisões.
        """
        if self.state == "countdown":
            now = time.time()
            if now - self.last_countdown_time > 1:
                self.countdown -= 1
                self.last_countdown_time = now
                if self.countdown <= 0:
                    self.start_game()
        elif self.state == "playing":
            self.player.update(keyboard)

            # Checar colisões e atualizar inimigos
            self.check_collisions()
            for enemy in self.enemies:
                enemy.move_towards(self.player)

    def check_collisions(self):
        """
        Verifica colisões entre o jogador e outros objetos, incluindo obstáculos, inimigos e porta.
        """
        # Checar colisão do jogador com obstáculos
        for obstacle in self.obstacles:
            if self.player.actor.colliderect(obstacle.actor):
                self.player.revert_position()
                self.play_ops()

        # Checar colisão do jogador com inimigos
        for enemy in self.enemies:
            if self.player.actor.colliderect(enemy.actor):
                self.player.health -= 10
                self.play_eep()

        # Verificar se o jogador perdeu
        if self.player.health <= 0:
            self.state = "game_over"

        # Checar colisão do jogador com a porta
        if self.player.actor.colliderect(self.door.actor):
            self.current_room += 1
            self.play_go()
            if self.current_room > 15:
                self.state = "game_won"
            else:
                self.start_game()

    def draw(self):
        """
        Desenha na tela com base no estado atual do jogo.
        """
        if self.state == "intro":
            self.capa.draw()
        elif self.state == "menu":
            self.capa_desfocada.draw()
            self.draw_menu()
        elif self.state == "countdown":
            screen.fill("black")
            screen.draw.text(f"{self.countdown}", center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="white")
        elif self.state == "playing":
            self.draw_game()
        elif self.state == "game_won":
            screen.fill((0, 45, 0))
            screen.draw.text("Você Venceu!", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="green")
        elif self.state == "game_over":
            self.draw_game_over()

    def draw_menu(self):
        """
        Desenha o menu principal na tela.
        """
        screen.draw.text("MENU", center=(WIDTH // 2, 100), fontsize=80, color="orange")
        for i, option in enumerate(self.menu_options):
            color = "black" if i == self.menu_selected else "black"
            screen.draw.text(option, center=(WIDTH // 2, 300 + i * 50), fontsize=60, color=color)

    def draw_game(self):
        screen.blit(fundo, (0, 0))
        self.player.draw()
        self.door.draw()
        for enemy in self.enemies:
            enemy.draw()
        for obstacle in self.obstacles:
            obstacle.draw()
        screen.draw.text(f"Sala: {self.current_room}", (10, 10), fontsize=28, color="white")
        screen.draw.text(f"Saúde: {self.player.health}", (10, 50), fontsize=28, color="white")

    def draw_game_over(self):
        """
        Desenha a tela de fim de jogo com as opções disponíveis.
        """
        screen.fill((0, 0, 0))
        screen.draw.text("Você Perdeu!", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=50, color="red")
        for i, option in enumerate(self.end_options):
            screen.draw.text(option, center=(WIDTH // 2, HEIGHT // 2 + 50 + i * 50), fontsize=40, color="white")

    def handle_menu_click(self, pos):
        """
        Lida com cliques no menu principal.

        Args:
            pos (tuple): Posição do clique do mouse.
        """
        for i, option in enumerate(self.menu_options):
            option_rect = Rect((WIDTH // 2 - 200, 300 + i * 50 - 20), (400, 40))
            if option_rect.collidepoint(pos):
                self.menu_selected = i
                if i == 0:  # Começar o jogo
                    self.state = "countdown"
                elif i == 1:  # Alternar som
                    self.sound_enabled = not self.sound_enabled
                    self.menu_options[1] = "Música e sons: Ligado" if self.sound_enabled else "Música e sons: Desligado"
                    if self.sound_enabled:
                        sounds.kalimba_game.play()
                    else:
                        sounds.kalimba_game.stop()
                elif i == 2:  # Sair
                    self.em_breve.draw()
                    time.sleep(2)
                    self.state = "exit"

    def handle_game_over_click(self, pos):
        """
        Lida com cliques na tela de fim de jogo.

        Args:
            pos (tuple): Posição do clique do mouse.
        """
        for i, option in enumerate(self.end_options):
            option_rect = Rect((WIDTH // 2 - 200, HEIGHT // 2 + 50 + i * 50 - 20), (400, 40))
            if option_rect.collidepoint(pos):
                if i == 0:  # Jogar Novamente
                    self.countdown = 3
                    self.state = "countdown"
                elif i == 1:  # Sair
                    self.em_breve.draw()
                    time.sleep(2)
                    self.state = "exit"

class Player:
    """
    Representa o jogador, implementar seus movimento e a animação dos sprites.
    """
    def __init__(self, x, y):
        self.health = 1000
        self.actor = Actor("player/player_stand_1", (x, y))
        self.sprites = {
            "stand": ["player/player_stand_1", "player/player_stand_2"],
            "walk": ["player/player_walk_1", "player/player_walk_2"]
        }
        self.last_position = self.actor.pos
        self.frame_index = 0
        self.last_frame_time = time.time()

    def update(self, keys):
        dx, dy = 0, 0
        moving = False
        self.last_position = self.actor.pos

        if keys.left:
            dx -= 5
            moving = True
        if keys.right:
            dx += 5
            moving = True
        if keys.up:
            dy -= 5
            moving = True
        if keys.down:
            dy += 5
            moving = True

        if moving:
            now = time.time()
            if now - self.last_frame_time > 0.2:
                self.frame_index = (self.frame_index + 1) % len(self.sprites["walk"])
                self.actor.image = self.sprites["walk"][self.frame_index]
                self.last_frame_time = now
        else:
            self.actor.image = self.sprites["stand"][self.frame_index]

        self.actor.x += dx
        self.actor.y += dy

    def revert_position(self):
        self.actor.pos = self.last_position

    def draw(self):
        self.actor.draw()

class Enemy:
    """
    Representa inimigos, implementar seus movimento e a animação dos sprites.
    """
    def __init__(self, x, y):
        self.actor = Actor("enemy/enemy_stand_1", (x, y))
        self.sprites = {
            "stand": ["enemy/enemy_stand_1", "enemy/enemy_stand_2"],
            "walk": ["enemy/enemy_walk_1", "enemy/enemy_walk_2"]
        }
        self.frame_index = 0
        self.last_frame_time = time.time()

    def move_towards(self, player):
        if player.actor.x > self.actor.x:
            self.actor.x += 2
        elif player.actor.x < self.actor.x:
            self.actor.x -= 2
        if player.actor.y > self.actor.y:
            self.actor.y += 2
        elif player.actor.y < self.actor.y:
            self.actor.y -= 2

        # Animação do inimigo
        now = time.time()
        if now - self.last_frame_time > 0.2:
            self.frame_index = (self.frame_index + 1) % len(self.sprites["walk"])
            self.actor.image = self.sprites["walk"][self.frame_index]
            self.last_frame_time = now

    def draw(self):
        self.actor.draw()

class Obstacle:
    """
    Representa as barreiras.
    """
    def __init__(self, x, y):
        self.actor = Actor("obstacle", (x, y))

    def draw(self):
        self.actor.draw()

class Door:
    """
    Representa a porta, que serve de passagem para outra sala.
    """
    def __init__(self, x, y):
        self.actor = Actor("door", (x, y))

    def draw(self):
        self.actor.draw()
"""
Objeto, game, que representa a classe Game, e roda os métodos criados.
"""
game = Game()

def draw():
    game.draw()

def update():
    game.update()

def on_mouse_down(pos):
    if game.state == "intro":
        game.state = "menu"
    elif game.state == "menu":
        game.handle_menu_click(pos)
    elif game.state == "game_over":
        game.handle_game_over_click(pos)

pgzrun.go()
