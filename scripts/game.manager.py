import pygame

class GameManager:
    def __init__(self):
        self.phase = 1
        self.score = 0
        self.phase_score_limit = 100  # Pontuação para avançar de fase

    def update_phase(self):
        if self.score >= self.phase * self.phase_score_limit:
            self.phase += 1

    def check_collision(self, player, enemy):
        player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
        enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        return player_rect.colliderect(enemy_rect)

    def increase_score(self, points):
        self.score += points
