import pygame

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
        self.game_font = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Escape the Maze")

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ['coin', 'door', 'monster', 'robot']:
            self.images.append(pygame.image.load(name + ".png"))

    def new_game(self):
        self.score = 0
        self.moves = 0

        self.map = self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                               [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 2, 3, 0, 0, 0, 1, 1, 1, 1],
                               [1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
                               [1, 2, 0, 0, 0, 0, 0, 1, 2, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
                               [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                               [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        
    def draw_window(self):
        self.window.fill((0, 0, 0))

        pygame.display.flip()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
    def main_loop(self):
        while True:
            self.check_events()
            self.draw_window()

if __name__ == "__main__":
    EscapeTheMaze()