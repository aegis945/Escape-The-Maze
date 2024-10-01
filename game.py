import pygame
from os import path
from random import sample, shuffle

class Robot:
    def __init__(self, scale: int, image: pygame.Surface):
        self.x = 1
        self.y = 1
        self.scale = scale
        self.image = image

    def move(self, dx: int, dy: int, game_map: list):
        new_x = self.x + dx
        new_y = self.y + dy

        if game_map[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

    def draw(self, window: pygame.Surface):
        window.blit(self.image, (self.x * self.scale, self.y * self.scale))

class Monster:
    def __init__(self, x: int, y: int, scale: int, image: pygame.Surface):
        self.x = x
        self.y = y
        self.scale = scale
        self.image = image
        self.move_delay = 300
        self.move_timer = 0

    def move(self, game_map):
        if self.move_timer > 0:
            self.move_timer -= 1
            return
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        shuffle(directions)

        for dx, dy in directions:
            if self.is_valid_move(dx, dy, game_map):
                self.x += dx 
                self.y += dy
                break

        self.move_timer = self.move_delay

    def is_valid_move(self, dx: int, dy: int, game_map: list):
        new_x, new_y = self.x + dx, self.y + dy

        return (0 <= new_x < len(game_map[0]) and 0 <= new_y < len(game_map) and game_map[new_y][new_x] == 0)

    def draw(self, window: pygame.Surface):
        window.blit(self.image, (self.x * self.scale, self.y * self.scale))
class EscapeTheMaze:
    def __init__(self):
        pygame.init()

        self.load_images()
        self.new_game()

        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height + self.scale))
        self.game_font = pygame.font.SysFont("None", 30)

        pygame.display.set_caption("Escape the Maze")

        self.robot = Robot(self.scale, self.images[4])
        self.monsters = []
        self.generate_monsters(3)

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ['floor', 'wall', 'door', 'monster', 'robot', 'coin']:
            image_path = path.join('images', name + ".png")
            self.images.append(pygame.image.load(image_path))

    def new_game(self):
        self.score = 0
        self.moves = 0

        self.map = [
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
                    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1],
                    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1],
                    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1],
                    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1],
                    [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1],
                    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1],
                    [1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
                    [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                    [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
                ]
        
        self.create_coins(30)
        
    def draw_window(self):
        self.window.fill((255, 255, 255))
        self.draw_maze()
        self.robot.draw(self.window)

        for monster in self.monsters:
            monster.draw(self.window)

        for coin in self.coins:
            coin_x, coin_y = coin
            self.window.blit(self.images[5], (coin_x * self.scale, coin_y * self.scale))

        score_text = self.game_font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_x = self.width * self.scale - score_text.get_width() - 10
        score_y = 10
        self.window.blit(score_text, (score_x, score_y))

        pygame.display.flip()

    def draw_maze(self):
        for y in range(self.height):
            for x in range(self.width):
                square = self.map[y][x]
                self.window.blit(self.images[square], (x * self.scale, y * self.scale))

    def create_coins(self, number_of_coins: int):
        self.coins = []
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == 0 and (x, y) != (1, 1):
                    self.coins.append((x, y))

        self.coins = sample(self.coins, number_of_coins)

    def generate_monsters(self, number_of_monsters: int):
        floor_positions = []
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile == 0:
                    floor_positions.append((x, y))

        valid_positions = []
        for x, y in floor_positions:
            if abs(x - self.robot.x) > 3 or abs(y - self.robot.y) > 3:
                valid_positions.append((x, y))

        monster_positions = sample(valid_positions, number_of_monsters)

        self.monsters = []
        for x, y in monster_positions:
            monster = Monster(x, y, self.scale, self.images[3])
            self.monsters.append(monster)

    def move_monsters(self):
        for monster in self.monsters:
            monster.move(self.map)

    def check_collisions(self):
        for monster in self.monsters:
            if monster.x == self.robot.x and monster.y == self.robot.y:
                self.game_over()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.robot.move(-1, 0, self.map)
                if event.key == pygame.K_UP:
                    self.robot.move(0, -1, self.map)
                if event.key == pygame.K_RIGHT:
                    self.robot.move(1, 0, self.map)
                if event.key == pygame.K_DOWN:
                    self.robot.move(0, 1, self.map)
                if event.key == pygame.K_ESCAPE:
                    exit()
            if event.type == pygame.QUIT:
                exit()

        if (self.robot.x, self.robot.y) in self.coins:
            self.coins.remove((self.robot.x, self.robot.y))
            self.score += 1
    
    def game_over(self):
        message = self.game_font.render(f"Game Over! Your score is {self.score}", True, (255, 0, 0))
        message_rect = message.get_rect(center=(self.width * self.scale // 2, self.height * self.scale // 2))

        pygame.draw.rect(self.window, (255, 255, 255), message_rect.inflate(20, 20))
        self.window.blit(message, message_rect)
        
        pygame.display.flip()
        pygame.time.wait(2000)
        exit()
    
    def game_solved(self):
        message = self.game_font.render(f"You escaped! Your total score is {self.score}", True, (0, 255, 0))
        message_rect = message.get_rect(center=(self.width * self.scale // 2, self.height * self.scale // 2))

        pygame.draw.rect(self.window, (255, 255, 255), message_rect.inflate(20, 20))
        self.window.blit(message, message_rect)
        
        pygame.display.flip()
        pygame.time.wait(2000)
        exit()
        
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()
            self.move_monsters()
            self.check_collisions()

            if self.map[self.robot.y][self.robot.x] == 2:
                self.game_solved()

if __name__ == "__main__":
    EscapeTheMaze()