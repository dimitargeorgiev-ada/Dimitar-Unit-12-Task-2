import pygame

pygame.init()
win = pygame.display.set_mode((720, 576), pygame.RESIZABLE)
pygame.display.set_caption("Train Simulator: Python Edition")
bg = pygame.image.load('Assets/bg.jpg')
clock = pygame.time.Clock()
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)


class Camera():
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    
    def apply(self, entity):
        return entity.x - self.camera.x, entity.y - self.camera.y
    
    def update(self, target):
        offset = -1200  # pixels from the left edge
        x = target.x - offset
        if x < 0:
            x = 0
        y = target.y - self.height // 2
        self.camera.x = x
        self.camera.y = y


class class171():
    walkRight = [pygame.image.load('Assets/171.png')]
    walkLeft = [pygame.image.load('Assets/171.png')]
    

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.vel = 0
        self.maxvel = 1000
        self.acc = 0.1
        self.size = 10
        figsize=(8, 6)

    def draw(self, win, draw_x=None, draw_y=None):
        if draw_x is None:
            draw_x = self.x
        if draw_y is None:
            draw_y = self.y
        win.blit(self.walkRight[0], (draw_x, draw_y))
        
    def move(self, move_right=False, move_left=False):
        if move_right:
            self.vel += 1
        if move_left:
            self.vel -= 1
        if self.vel > self.maxvel:
            self.vel = self.maxvel
        if self.vel < -self.maxvel:
            self.vel = -self.maxvel
        if self.vel < 0:
            self.vel = 0

        self.x += self.vel * self.acc


def redrawGameWindow():
    bg_width = bg.get_width()
    bg_height = bg.get_height()
    cam_x = camera.camera.x
    cam_y = camera.camera.y
    start_x = -(cam_x % bg_width)
    for i in range(-1, win.get_width() // bg_width + 2):
        win.blit(bg, (start_x + i * bg_width, -cam_y))
    draw_x, draw_y = camera.apply(class171)
    class171.draw(win, draw_x, draw_y)
    pygame.display.update()

class171 = class171(20, 310, 64, 64, 450)

camera = Camera(500, 480)

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    move_right = keys[pygame.K_w]
    move_left = keys[pygame.K_s]
    class171.move(move_right, move_left)
    camera.update(class171)
    text_surface = my_font.render('Some Text', False, (0, 0, 0))
    print("Speed:", class171.vel * class171.acc, "mph")
    redrawGameWindow()



pygame.quit()