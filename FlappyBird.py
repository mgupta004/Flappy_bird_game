import pygame
import os
import random

pygame.init()

# Game window size
WIDTH = 500
HEIGHT = 800

# Load sounds
pygame.mixer.init()
WING_SOUND = pygame.mixer.Sound(os.path.join("sounds", "wing.wav"))
POINT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "point.wav"))
HIT_SOUND = pygame.mixer.Sound(os.path.join("sounds", "hit.wav"))

# Load images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)


class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -4
        self.tick_count = 0
        self.height = self.y
        WING_SOUND.play()

    def move(self):
        self.tick_count += 1
        d = self.vel * self.tick_count + 0.5 * self.tick_count ** 2

        if d >= 14:
            d = 14
        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count >= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return t_point or b_point


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))
    for pipe in pipes:
        pipe.draw(win)
    text = STAT_FONT.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))
    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def welcome_screen(win):
    title_font = pygame.font.SysFont("comicsans", 60)
    info_font = pygame.font.SysFont("comicsans", 40)

    title_text = title_font.render("Flappy Bird", True, (255, 255, 255))
    info_text = info_font.render("Press SPACE to Start", True, (255, 255, 255))

    run = True
    while run:
        win.blit(BG_IMG, (0, 0))
        win.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 3))
        win.blit(info_text, ((WIDTH - info_text.get_width()) // 2, HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False


def game_over_screen(win, score):
    title_font = pygame.font.SysFont("comicsans", 30)
    info_font = pygame.font.SysFont("comicsans", 40)

    title_text = title_font.render("Game Over", True, (255, 0, 0))
    score_text = info_font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = info_font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    HIT_SOUND.play()
    run = True
    while run:
        win.blit(BG_IMG, (0, 0))
        win.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 4))
        win.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 - 30))
        win.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2 + 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    score = 0
    welcome_screen(win)

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.move()
        base.move()

        add_pipe = False
        rem = []

        for pipe in pipes:
            pipe.move()
            if pipe.collide(bird):
                game_over_screen(win, score)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            score += 1
            POINT_SOUND.play()
            pipes.append(Pipe(WIDTH))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
            game_over_screen(win, score)

        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()


main()
