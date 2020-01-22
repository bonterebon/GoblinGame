import pygame


class Goblin(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_count = 0
        self.velocity = 5
        self.right = True
        self.left = True
        self.up = False
        self.down = False
        self.is_walking = False

        self.left_idle_images = [pygame.image.load('images/goblin_left_idle_1.png').convert_alpha(),
                                 pygame.image.load('images/goblin_left_idle_2.png').convert_alpha()]
        self.left_idle_images = self.scale_sprites(self.left_idle_images)
        self.right_idle_images = [pygame.image.load('images/goblin_right_idle_1.png').convert_alpha(),
                                 pygame.image.load('images/goblin_right_idle_2.png').convert_alpha()]
        self.right_idle_images = self.scale_sprites(self.right_idle_images)

        self.left_walk_images = [pygame.image.load('images/goblin_left_walk_1.png').convert_alpha(),
                                 pygame.image.load('images/goblin_left_walk_2.png').convert_alpha()]
        self.left_walk_images = self.scale_sprites(self.left_walk_images)
        self.right_walk_images = [pygame.image.load('images/goblin_right_walk_1.png').convert_alpha(),
                                 pygame.image.load('images/goblin_right_walk_2.png').convert_alpha()]
        self.right_walk_images = self.scale_sprites(self.right_walk_images)

        self.width = self.left_idle_images[0].get_size()[0]
        self.height = self.left_idle_images[0].get_size()[1] - 20
        print(self.x, self.y)
        print(self.width, self.height)
        self.hitbox = (self.x + 5, self.y + 20, self.width - 10, self.height)
        print(self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3])

    def scale_sprites(self, sprites):
        scaled = []
        for i in sprites:
            scaled.append(pygame.transform.scale(i, (i.get_size()[0] * 2, i.get_size()[1] * 2)))
        return scaled

    def draw(self, window):
        if (self.animation_count + 1) > 2:
            self.animation_count = 0
        if self.is_walking:
            if self.left:
                window.blit(self.left_walk_images[self.animation_count], (self.x, self.y))
            elif self.right:
                window.blit(self.right_walk_images[self.animation_count], (self.x, self.y))
        else:
            if self.left:
                window.blit(self.left_idle_images[self.animation_count], (self.x, self.y))
            if self.right:
                window.blit(self.right_idle_images[self.animation_count], (self.x, self.y))
        self.animation_count += 1
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2) # draws self.hitbox

    def move(self, direction):
        if direction == 'r':
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.x += self.velocity
        elif direction == 'l':
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.x -= self.velocity
        elif direction == 'u':
            self.up = True
            self.right = False
            self.left = False
            self.down = False
            self.y -= self.velocity
        elif direction == 'd':
            self.down = True
            self.right = False
            self.left = False
            self.up = False
            self.y += self.velocity
        self.hitbox = (self.x + 5, self.y + 20, self.width - 10, self.height)
        print(self.x, self.y)
        print('--')
        print(self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3])


class Game(object):
    def __init__(self, width=400, height=300, fps=5):
        pygame.init()
        pygame.display.set_caption('Goblin game')
        self.width = width
        self.height = height
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.main_window = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont('mono', 10)
        self.goblin = Goblin(150, 10)

    def redraw_window(self):
        self.main_window.fill((0, 0, 0))
        self.goblin.draw(self.main_window)

        pygame.display.update()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT\
                            or event.key == pygame.K_d:
                        self.goblin.is_walking = False


            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.goblin.x < self.width - self.goblin.width:
                self.goblin.is_walking = True
                self.goblin.move('r')
            elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.goblin.hitbox[0] - self.goblin.velocity >= 0:
                self.goblin.is_walking = True
                self.goblin.move('l')
            elif keys[pygame.K_UP] or keys[pygame.K_w] and self.goblin.hitbox[1] > 0:
                self.goblin.is_walking = True
                self.goblin.move('u')
            elif keys[pygame.K_DOWN] or keys[pygame.K_s] and self.goblin.hitbox[1] <= self.height - self.goblin.hitbox[3]\
                    - self.goblin.velocity:
                self.goblin.is_walking = True
                self.goblin.move('d')
            self.redraw_window()


if __name__ == '__main__':
    Game().run()
