# Césio Hazard

## Requisitos
- Python >= 3.x
- `pip` para gerenciar dependências
- PgZero
- Pygame (apenas para a classe `Rect`)

## Instalação
1. Clone o repositório:
   ```bash
   git clone git@github.com:ml5w3s/cesio-hazard.git
# Jogo de Sobrevivência Top-Down

Um jogo simples inspirado em mecânicas de sobrevivência top-down, onde o jogador precisa, acessar uma porta, para passar de sala, evitando inimigos que o perseguem e causam dano ao chegar muito perto.

## Como Jogar

- **Movimento**: Use as setas do teclado para mover o jogador (azul) pela tela.
- **Objetivo**: Chegar na 15º sala e sobreviver, enquanto evita os inimigos (verde).
- **Dano**: Se um inimigo se aproximar muito, o jogador perde saúde.

## Como Executar

1. Certifique-se de que as dependências estão instaladas:
   ```bash
   pip install pgzero
   cd cesio-hazard
   pgzrun /src/game_cesio.py
