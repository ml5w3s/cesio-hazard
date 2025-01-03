from pygame import Rect
import random

# Configuração da tela
WIDTH = 800  #: Largura da tela.
HEIGHT = 600  #: Altura da tela.

# Jogador e inimigos
player = Rect(400, 300, 32, 32)  #: Retângulo representando o jogador.
enemies = [
    Rect(random.randint(0, WIDTH - 32), random.randint(0, HEIGHT - 32), 32, 32)
    for _ in range(5)
]  #: Lista de inimigos representados como retângulos.

# Saúde do jogador
player_health = 100  #: Quantidade inicial de saúde do jogador.


def draw():
    """
    Desenha os elementos do jogo na tela.

    A função é chamada automaticamente pelo PgZero para renderizar os elementos do jogo.
    Ela desenha o jogador, os inimigos e exibe a saúde do jogador na tela.
    """
    screen.fill((0, 0, 0))  # Fundo preto
    screen.draw.filled_rect(player, "blue")  # Jogador em azul
    for enemy in enemies:
        screen.draw.filled_rect(enemy, "red")  # Inimigos em vermelho
    screen.draw.text(f"Saúde: {player_health}", (10, 10), color="white")  # Exibe saúde


def update():
    """
    Atualiza a lógica do jogo.

    A função é chamada automaticamente pelo PgZero para atualizar os estados do jogo.
    Controla a movimentação do jogador e dos inimigos, além de verificar colisões e aplicar dano.

    Global:
        player_health (int): A saúde do jogador, que diminui ao colidir com os inimigos.
    """
    global player_health

    # Movimentação do jogador
    if keyboard.left:
        player.x -= 5
    if keyboard.right:
        player.x += 5
    if keyboard.up:
        player.y -= 5
    if keyboard.down:
        player.y += 5

    # Movimentação dos inimigos e lógica de dano
    for enemy in enemies:
        if player.x > enemy.x:
            enemy.x += 2
        if player.x < enemy.x:
            enemy.x -= 2
        if player.y > enemy.y:
            enemy.y += 2
        if player.y < enemy.y:
            enemy.y -= 2

        # Causar dano se os inimigos estiverem muito próximos
        if player.colliderect(enemy):
            player_health -= 1
