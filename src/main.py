from pgzero.actor import Actor  # Importa a classe Actor para gerenciar sprites
import random

class Character:
    """
    Classe base para personagens com movimento e animação.
    """

    def __init__(self, animations, initial_state, position):
        self.animations = animations
        self.state = initial_state
        self.actor = Actor(animations[initial_state][0], position)
        self.frame = 0
        self.frame_timer = 0
        self.x, self.y = position

    def update_position(self, dx=0, dy=0):
        self.x += dx
        self.y += dy
        self.actor.pos = (self.x, self.y)

    def set_state(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.frame = 0

    def update_animation(self):
        self.frame_timer += 1
        if self.frame_timer >= 5:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % len(self.animations[self.state])
            self.actor.image = self.animations[self.state][self.frame]

    def draw(self):
        self.actor.draw()


class Player(Character):
    """
    Classe para o jogador.
    """

    def handle_input(self, keyboard):
        dx = dy = 0
        if keyboard.left:
            dx -= 5
        if keyboard.right:
            dx += 5
        if keyboard.up:
            dy -= 5
        if keyboard.down:
            dy += 5

        self.set_state("walk" if dx != 0 or dy != 0 else "stand")
        self.update_position(dx, dy)


class Enemy(Character):
    """
    Classe para os inimigos.
    """

    def follow(self, target):
        dx = dy = 0
        if target[0] > self.x:
            dx += 2
        if target[0] < self.x:
            dx -= 2
        if target[1] > self.y:
            dy += 2
        if target[1] < self.y:
            dy -= 2

        self.set_state("walk" if dx != 0 or dy != 0 else "stand")
        self.update_position(dx, dy)
