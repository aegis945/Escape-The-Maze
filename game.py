import pygame
from os import path

class Robot:
    def __init__(self, scale: int):
        self.x = 1
        self.y = 1
        self.scale = scale
        self.image = pygame.image.load(path.join('images', 'robot.png'))

    def move(self, dx: int, dy: int, game_map: list):
        new_x = self.x + dx
        new_y = self.y + dy

        if game_map[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y

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

        self.robot = Robot(self.scale)

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
        
    def draw_window(self):
        self.window.fill((255, 255, 255))
        self.draw_maze()
        self.robot.draw(self.window)

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

    def game_solved(self):
        message = self.game_font.render("You escaped!", True, (0, 255, 0))
        message_rect = message.get_rect(center=(self.width * self.scale // 2, self.height * self.scale // 2))
        self.window.blit(message, (self.scale, self.height * self.scale))
        pygame.draw.rect(self.window, (255, 255, 255), message_rect.inflate(20, 20))
        self.window.blit(message, message_rect)
        
        pygame.display.flip()
        pygame.time.wait(2000)
        exit()
        
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

            if self.map[self.robot.y][self.robot.x] == 2:
                self.game_solved()

if __name__ == "__main__":
    EscapeTheMaze()