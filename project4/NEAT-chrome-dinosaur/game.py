import pygame
import os
import random
import sys
import math
import neat

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Sprites
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput == "jump" and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput == "duck" and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput == "duck"):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        rand = random.randint(0, 3)
        if(rand == 0):
            self.rect.y = 300
        else:
            self.rect.y = 200
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


# calcula e printa o score do jogo
def score():
    global points, game_speed
    font = pygame.font.Font('freesansbold.ttf', 20)
    
    points += 1
    if points % 100 == 0 and game_speed < 40:
        game_speed += 1
    
    text = font.render("Pontos: " + str(points), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (1000, 40)
    SCREEN.blit(text, textRect)


# printa as estatisticas da geração atual
def statistics():
    global dinosaurs, game_speed, ge
    font = pygame.font.Font('freesansbold.ttf', 20)

    text_1 = font.render(f'Dinossauros Vivos:  {str(len(dinosaurs))}', True, (0, 0, 0))
    text_2 = font.render(f'Geração:  {p.generation+1}', True, (0, 0, 0))
    text_3 = font.render(f'Velocidade do Jogo:  {str(game_speed)}', True, (0, 0, 0))

    SCREEN.blit(text_1, (50, 450))
    SCREEN.blit(text_2, (50, 480))
    SCREEN.blit(text_3, (50, 510))


def background():
    global x_pos_bg, y_pos_bg
    
    image_width = BG.get_width()
    SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
    SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
    
    if x_pos_bg <= -image_width:
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        x_pos_bg = 0

    x_pos_bg -= game_speed


def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2+dy**2)


def eval_genomes(genomes, config):
    
    global game_speed, x_pos_bg, y_pos_bg, points, dinosaurs, obstacles, nets, ge

    run = True
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 20)
    
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0

    cloud = Cloud()
    dinosaurs = []
    obstacles = []
    nets = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinosaurs.append(Dinosaur())
        ge.append(genome)

    # loop principal
    while run:
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        for dinosaur in dinosaurs:
            dinosaur.update("run")
            dinosaur.draw(SCREEN)

        if len(dinosaurs) == 0:
            break

        if points > 4000:
            break;

        # calcula output
        if len(obstacles) == 1:
            obstacle = obstacles[0]

            for i, dinosaur in enumerate(dinosaurs):
                ge[i].fitness += 0.1

                output = nets[i].activate((
                    dinosaur.dino_rect.y, # coord y do dino
                    obstacle.rect.y, # coord y do obstaculo
                    obstacle.rect.width, # largura do obstaculo
                    obstacle.rect.height, # altura do obstaculo
                    abs(dinosaur.dino_rect.x + dinosaur.dino_rect.width - obstacle.rect.x), # distancia
                    game_speed # velocidade do jogo
                ))

                if output[0] > 0.5 and not dinosaur.dino_jump and not dinosaur.dino_duck:
                    dinosaur.update("duck")
                elif output[0] <= 0.5 and not dinosaur.dino_jump and dinosaur.dino_duck:
                    dinosaur.update("run")
                elif output[1] > 0.5 and not dinosaur.dino_jump and not dinosaur.dino_duck:
                    dinosaur.update("jump")

        # adiciona obstaculo
        if len(obstacles) == 0:
            num = random.randint(0, 10)
            if num < 3:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif num < 6:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        # colisao
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    dinosaurs.pop(i)
                    nets.pop(i)
                    ge.pop(i)

        background()
        cloud.draw(SCREEN)
        cloud.update()
        score()
        statistics()
        clock.tick(30)
        pygame.display.update()


def run(config_path):

    global p

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    p = neat.Population(config)

    # imprime no terminal as infos
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "configBird.txt")
    run(config_path)