import pygame

#Setup
pygame.init()
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("First Game")
bg = pygame.image.load('Assets/bg.jpg')
font = pygame.font.Font(None, 28)
clock = pygame.time.Clock()


class class171:
    WALK_IMG = pygame.image.load('Assets/171.png')

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end

        # Movement state
        self.vel = 0.0
        self.accel_dir = 0
        self.acceleration = 0.15
        self.maxspeed = 100.0

    def handle_input(self, keys):
        # W moves forward (right), S moves backward (left)
        if keys[pygame.K_w]:
            self.accel_dir = 1
        elif keys[pygame.K_s]:
            self.accel_dir = -1
        else:
            self.accel_dir = 0

    def move(self):
        if self.accel_dir != 0:
            self.vel += self.accel_dir * self.acceleration
            self.vel = max(-self.maxspeed, min(self.maxspeed, self.vel))

        # Keep current speed when no key is held (no friction applied)
        self.x += self.vel

    def draw(self, win, camera_x):
        self.move()
        draw_x = self.x - camera_x
        # Draw on the right-hand side of the screen when camera follows the object
        if self.vel >= 0:
            win.blit(self.WALK_IMG, (draw_x, self.y))
        else:
            win.blit(self.WALK_IMG, (draw_x, self.y))



#                      --- Draw a Frame ---

def redrawGameWindow(player, camera_x):
    # Looping background
    bg_w = bg.get_width()
    offset_x = -(camera_x % bg_w)

    # Draw enough tiles to cover the screen even when scrolling
    win.blit(bg, (offset_x - bg_w, 0))
    win.blit(bg, (offset_x, 0))
    win.blit(bg, (offset_x + bg_w, 0))

    player.draw(win, camera_x)

    # Speedometer
    speed_text = font.render(f"Speed: {abs(player.vel):.1f}", True, (255, 255, 255))
    win.blit(speed_text, (10, 10))

    pygame.display.update()

#                      --- Main Game Loop ---

# My train-like object (startX, y, width, height, endX)
train = class171(20, 310, 64, 64, 450)

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    train.handle_input(keys)

    # Camera follows the train, keeping it toward the right side of the screen
    camera_x = (train.x + train.width) - win.get_width() * 0.2

    # Draw
    redrawGameWindow(train, camera_x)

pygame.quit()


