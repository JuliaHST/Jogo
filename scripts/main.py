import pygame
import random
import json
import sys
from datetime import datetime

pygame.init()

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Food Drop Game")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Carregar imagens
background_image = pygame.image.load(r"C:\Users\17064192608\joguito\Food Drop\assets\images\fundo.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load(r"C:\Users\17064192608\joguito\Food Drop\assets\images\player.png")
good_food_image = pygame.image.load(r"C:\Users\17064192608\joguito\Food Drop\assets\images\good_food.png")
bad_food_image = pygame.image.load(r"C:\Users\17064192608\joguito\Food Drop\assets\images\bad_food.png")

# Ajustar tamanhos das imagens
player_image = pygame.transform.scale(player_image, (100, 100))
good_food_image = pygame.transform.scale(good_food_image, (50, 50))
bad_food_image = pygame.transform.scale(bad_food_image, (50, 50))

# Fontes
font = pygame.font.SysFont("comicsansms", 30)

def draw_text(text, x, y, color=BLACK, shadow=False):
    text_surface = font.render(text, True, color)
    if shadow:
        shadow_surface = font.render(text, True, (100, 100, 100))  # Cor da sombra
        screen.blit(shadow_surface, (x + 3, y + 3))  # Sombra deslocada
    screen.blit(text_surface, (x, y))

# Classes
class Player:
    def __init__(self, name):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 10
        self.score = 0
        self.lives = 5
        self.name = name

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Restringir ao limite da tela
        self.x = max(0, min(SCREEN_WIDTH - 50, self.x))

    def draw(self):
        screen.blit(player_image, (self.x, self.y))

class Food:
    def __init__(self, x, y, good=True, speed=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.good = good

    def move(self):
        self.y += self.speed

    def draw(self):
        if self.good:
            screen.blit(good_food_image, (self.x, self.y))
        else:
            screen.blit(bad_food_image, (self.x, self.y))

class Inimigo:
    def __init__(self, speed=5):
        self.x = random.randint(20, SCREEN_WIDTH - 40)
        self.y = random.randint(-200, -20)
        self.speed = speed

    def move(self):
        self.y += self.speed

    def draw(self):
        # Carregar a imagem do inimigo uma única vez
        bad_food_image = pygame.image.load(r"C:\Users\17064192608\joguito\Food Drop\assets\images\bad_food.png")
        bad_food_image = pygame.transform.scale(bad_food_image, (40, 40))
        screen.blit(bad_food_image, (self.x, self.y))

# Funções para gerenciar o ranking
def save_ranking(player_name, score):
    try:
        # Carregar o ranking do arquivo
        with open('ranking.json', 'r') as file:
            ranking = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        ranking = []

    # Adicionar o novo jogador ao ranking
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ranking.append({'name': player_name, 'score': score, 'date': date})

    # Ordenar o ranking pela pontuação
    ranking = sorted(ranking, key=lambda x: x['score'], reverse=True)

    # Limitar a quantidade de resultados exibidos (Top 5)
    ranking = ranking[:5]

    # Salvar o ranking no arquivo
    with open('ranking.json', 'w') as file:
        json.dump(ranking, file, indent=4)

def load_ranking():
    try:
        with open('ranking.json', 'r') as file:
            ranking = json.load(file)
        return ranking
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função para pedir o nome do jogador no início
def get_player_name():
    input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3, SCREEN_WIDTH // 2, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font_input = pygame.font.Font(None, 36)
    text_surface = font_input.render(text, True, color)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill(WHITE)
        color = color_active if active else color_inactive
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font_input.render(text, True, color)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Função para exibir o ranking
def show_ranking():
    ranking = load_ranking()
    y_offset = SCREEN_HEIGHT // 4
    screen.fill(WHITE)
    draw_text("TOP 5 Ranking", SCREEN_WIDTH // 3, y_offset - 50)
    y_offset += 50

    for entry in ranking:
        draw_text(f"{entry['name']} - {entry['score']} points", SCREEN_WIDTH // 4, y_offset)
        y_offset += 40

    pygame.display.flip()
    pygame.time.wait(5000)  # Exibe o ranking por 5 segundos

# Inicialização
player_name = get_player_name()  # Solicitar nome do jogador
player = Player(player_name)
game_running = True
foods = []
enemies = []
phase = 1
phase_speed_increase = 1  # Incremento da velocidade dos inimigos e alimentos

# Função para resetar alimentos e inimigos
def reset_foods_and_enemies():
    global foods, enemies, phase_speed_increase
    foods.clear()
    enemies.clear()
    
    # A cada fase, aumenta a quantidade de alimentos e inimigos
    for _ in range(10 + phase * 2):  # Aumenta a quantidade de alimentos conforme as fases
        x = random.randint(20, SCREEN_WIDTH - 40)
        y = random.randint(-200, -20)
        good = random.choice([True, False])
        foods.append(Food(x, y, good, speed=5 + phase_speed_increase))  # Aumenta a velocidade com as fases
    for _ in range(5 + phase):  # Aumenta a quantidade de inimigos conforme as fases
        enemies.append(Inimigo(speed=5 + phase_speed_increase))  # Aumenta a velocidade dos inimigos com as fases

reset_foods_and_enemies()

# Loop principal do jogo
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()
    player.move(keys)

    # Atualizar a tela
    screen.blit(background_image, (0, 0))
    player.draw()

    for food in foods:
        food.move()
        food.draw()
        if food.y > SCREEN_HEIGHT:
            foods.remove(food)
            reset_foods_and_enemies()  # Resetar alimentos e inimigos se saírem da tela
        if player.x < food.x < player.x + 100 and player.y < food.y < player.y + 100:
            if food.good:
                player.score += 1
            else:
                player.lives -= 1
            foods.remove(food)

    for enemy in enemies:
        enemy.move()
        enemy.draw()
        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)
            reset_foods_and_enemies()  # Resetar inimigos se saírem da tela
        if player.x < enemy.x < player.x + 100 and player.y < enemy.y < player.y + 100:
            player.lives -= 1
            enemies.remove(enemy)

    if player.score // 2 > phase:
        phase += 1
        reset_foods_and_enemies()

        # Exibir a mensagem de transição de fase
        draw_text(f"Fase {phase}!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, color=BLUE, shadow=True)
        pygame.display.flip()
        pygame.time.wait(2000)  # Exibir a mensagem por 2 segundos

    # Exibir informações
    draw_text(f"Score: {player.score}", 10, 10)
    draw_text(f"Lives: {player.lives}", SCREEN_WIDTH - 150, 10)

    if player.lives <= 0:
        save_ranking(player.name, player.score)
        show_ranking()
        game_running = False

    pygame.display.flip()
    pygame.time.Clock().tick(60)
    
pygame.quit()
