import time
import random
import pgzrun
from pgzero.actor import Actor

# Configurações da tela
WIDTH = 800
HEIGHT = 600

# Configurações de som
sound_enabled = True

class Player:
    def __init__(self, x, y):
        self.health = 1000
        self.actor = Actor("player/player_stand_1", (x, y))
        self.sprites = {
            "stand": ["player/player_stand_1", "player/player_stand_2"],
            "walk": ["player/player_walk_1", "player/player_walk_2"]
        }
        self.frame_index = 0
        self.last_frame_time = time.time()

    def update(self, keys):
        dx, dy = 0, 0
        moving = False

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

    def draw(self):
        self.actor.draw()

class Enemy:
    def __init__(self, x, y):
        self.actor = Actor("enemy/enemy_stand_1", (x, y))
        self.sprites = {
            "stand": ["enemy/enemy_stand_1", "enemy/enemy_stand_2"],
            "walk": ["enemy/enemy_walk_1", "enemy/enemy_walk_2"]
        }
        self.frame_index = 0

    def move_towards(self, player):
        if player.actor.x > self.actor.x:
            self.actor.x += 2
        elif player.actor.x < self.actor.x:
            self.actor.x -= 2
        if player.actor.y > self.actor.y:
            self.actor.y += 2
        elif player.actor.y < self.actor.y:
            self.actor.y -= 2

    def draw(self):
        self.actor.draw()

class Obstacle:
    def __init__(self, x, y):
        self.actor = Actor("obstacle", (x, y))

    def draw(self):
        self.actor.draw()

class Door:
    def __init__(self, x, y):
        self.actor = Actor("door", (x, y))

    def draw(self):
        self.actor.draw()

class Game:
    def __init__(self):
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

        # Intro
        self.capa = Actor("capa", (WIDTH // 2, HEIGHT // 2))
        self.capa_desfocada = Actor("capa_desfocada", (WIDTH // 2, HEIGHT // 2))
        self.em_breve = Actor("em_breve", (WIDTH // 2, HEIGHT // 2))

    def start_game(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)
        self.door = Door(WIDTH - 50, HEIGHT // 2)
        self.enemies = [Enemy(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)) for _ in range(3)]
        self.obstacles = [
            Obstacle(200, 150),
            Obstacle(400, 400),
            Obstacle(600, 200)
        ]
        self.state = "playing"

    def draw(self):
        if self.state == "intro":
            self.capa.draw()
        elif self.state == "menu":
            self.capa_desfocada.draw()
            screen.draw.text("MENU", center=(WIDTH // 2, 100), fontsize=80, color="green")
        elif self.state == "countdown":
            screen.fill("black")
            screen.draw.text(f"{self.countdown}", center=(WIDTH // 2, HEIGHT // 2), fontsize=100, color="white")
        elif self.state == "playing":
            screen.fill("black")
            self.player.draw()
            self.door.draw()
            for enemy in self.enemies:
                enemy.draw()
            for obstacle in self.obstacles:
                obstacle.draw()
        elif self.state == "exit":
            self.em_breve.draw()

    def update(self):
        if self.state == "countdown":
            now = time.time()
            if now - self.last_countdown_time > 1:
                self.countdown -= 1
                self.last_countdown_time = now
                if self.countdown <= 0:
                    self.start_game()
        elif self.state == "playing":
            self.player.update(keyboard)
            for enemy in self.enemies:
                enemy.move_towards(self.player)

game = Game()

def draw():
    game.draw()

def update():
    game.update()

def on_mouse_down(pos):
    if game.state == "intro":
        game.state = "menu"
    elif game.state == "menu":
        game.state = "countdown"

pgzrun.go()
