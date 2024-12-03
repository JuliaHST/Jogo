import pygame
import random
import requests
import sys

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
font = pygame.font.SysFont("comicsansms", 40)

def draw_text(text, x, y, color=BLACK, shadow=False):
    text_surface = font.render(text, True, color)
    if shadow:
        shadow_surface = font.render(text, True, (100, 100, 100))  # Cor da sombra
        screen.blit(shadow_surface, (x + 3, y + 3))  # Sombra deslocada
    screen.blit(text_surface, (x, y))

# Classes
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 70
        self.speed = 7
        self.score = 0
        self.lives = 3

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
        bad_food_image = pygame.transform.scale(bad_food_image, (50, 50))
        screen.blit(bad_food_image, (self.x, self.y))

# Integração com Django
class DjangoIntegration:
    @staticmethod
    def save_score(player_name, score):
        try:
            response = requests.post("http://127.0.0.1:8000/api/scores/", data={"name": player_name, "score": score})
            if response.status_code == 201:
                print("Pontuação salva com sucesso!")
            else:
                print("Erro ao salvar pontuação.")
        except Exception as e:
            print(f"Erro ao conectar com o servidor: {e}")

# Inicialização
player = Player()
game_running = True
foods = []
enemies = []
phase = 1
phase_speed_increase = 1  # Incremento da velocidade dos inimigos e alimentos

# Função para resetar alimentos e inimigos
def reset_foods_and_enemies():
    global foods, enemies
    foods.clear()
    enemies.clear()
    for _ in range(10):
        x = random.randint(20, SCREEN_WIDTH - 40)
        y = random.randint(-200, -20)
        good = random.choice([True, False])
        foods.append(Food(x, y, good, speed=5 + phase_speed_increase))  # Aumentar a velocidade com as fases
    for _ in range(3):  # Número fixo de inimigos (reduzido de acordo com sua solicitação)
        enemies.append(Inimigo(speed=5 + phase_speed_increase))  # Aumentar a velocidade dos inimigos

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
        if (food.y + 50 > player.y) and (food.x < player.x + 100) and (food.x + 50 > player.x):
            player.score += 1 if food.good else -1
            foods.remove(food)

    for enemy in enemies[:]:  # Iterar sobre uma cópia da lista de inimigos
        enemy.move()
        enemy.draw()

        if enemy.y > SCREEN_HEIGHT:
            enemies.remove(enemy)
            reset_foods_and_enemies()  # Resetar alimentos e inimigos se saírem da tela
        
        # Colisão com o player
        if (enemy.y + 50 > player.y) and (enemy.x < player.x + 100) and (enemy.x + 50 > player.x):
            player.lives -= 1
            enemies.remove(enemy)  # Remover o inimigo após a colisão

    # Atualizar fase
    if player.score >= phase * 100:
        phase += 1
        phase_speed_increase += 1  # Aumentar a dificuldade
        reset_foods_and_enemies()  # Resetar alimentos e inimigos com nova dificuldade

    # Exibir informações
    draw_text(f"Fase: {phase}", SCREEN_WIDTH // 2 - 50, 10, color=BLUE)
    draw_text(f"Pontos: {player.score}", 10, 10)
    draw_text(f"Vidas: {player.lives}", SCREEN_WIDTH - 150, 10)

    if player.lives <= 0:
        draw_text("Game Over", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, color=RED, shadow=True)
        pygame.display.flip()
        pygame.time.delay(2000)
        game_running = False

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
