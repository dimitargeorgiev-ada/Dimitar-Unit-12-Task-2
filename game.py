import pygame
import os


pygame.init()
win = pygame.display.set_mode((720, 576), pygame.RESIZABLE)
pygame.display.set_caption("Train Simulator: Python Edition")
bg = pygame.image.load('Assets/images/bg.jpg')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)


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
    walkRight = [pygame.image.load('Assets/images/171.png')]
    walkLeft = [pygame.image.load('Assets/images/171.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.vel = 0
        self.maxvel = 1000
        self.acc = 0.1
        self.size = 5
        self.idle_sound = pygame.mixer.Sound('assets/audio/trains/171/idle.ogg')
        self.idle_playing = False
        self.accelerating_sound = pygame.mixer.Sound('assets/audio/trains/171/accdelarating.ogg')
        self.accelerating_playing = False
        self.horn_sound = pygame.mixer.Sound('assets/audio/trains/171/horn.ogg')
        self.last_horn_time = 0
        self.door_open_sound = pygame.mixer.Sound('assets/audio/trains/171/door open.ogg')
        self.door_close_sound = pygame.mixer.Sound('assets/audio/trains/171/door close.ogg')
        self.door_channel = pygame.mixer.Channel(0)
        self.door_sequence_active = False
        self.movement_disabled = False
        self.door_phase = 0  # 0: none, 1: opening, 2: waiting, 3: closing
        self.door_timer = 0
        self.door_open_length = self.door_open_sound.get_length() * 1000
        self.door_close_length = self.door_close_sound.get_length() * 1000
        self.total_door_sequence_length = self.door_open_length + 15000 + self.door_close_length
        self.sequence_start_time = 0
        self.prev_vel = 0
        figsize=(8, 6)

    def draw(self, win, draw_x=None, draw_y=None):
        if draw_x is None:
            draw_x = self.x
        if draw_y is None:
            draw_y = self.y
        win.blit(self.walkRight[0], (draw_x, draw_y))
        
    def move(self, move_right=False, move_left=False):
        if self.movement_disabled:
            return
        self.prev_vel = self.vel
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

        accelerating = self.vel > self.prev_vel

        if accelerating:
            if not self.accelerating_playing:
                self.accelerating_sound.play(loops=-1)
                self.accelerating_playing = True
            if self.idle_playing:
                self.idle_sound.stop()
                self.idle_playing = False
        else:
            if self.accelerating_playing:
                self.accelerating_sound.stop()
                self.accelerating_playing = False
            if not self.idle_playing:
                self.idle_sound.play(loops=-1)
                self.idle_playing = True

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
    speed_text = font.render(f"Speed: {class171.vel * class171.acc:.1f} mph", True, (255, 255, 255))
    win.blit(speed_text, (10, 10))
    if class171.door_phase > 0 and class171.door_phase < 3:
        elapsed = pygame.time.get_ticks() - class171.sequence_start_time
        visible_sequence_length = class171.door_open_length + 15000  # Opening + waiting only
        progress = min(elapsed / visible_sequence_length, 1.0)
        if progress < 1.0:
            bar_width = 300
            bar_height = 20
            bar_x = (win.get_width() - bar_width) // 2
            bar_y = win.get_height() - 50
            # White outline
            pygame.draw.rect(win, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
            # Steel blue fill
            pygame.draw.rect(win, (70, 130, 180), (bar_x, bar_y, bar_width * progress, bar_height))
            # Text
            loading_text = font.render("Loading Passengers", True, (255, 255, 255))
            text_rect = loading_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
            win.blit(loading_text, text_rect)
    pygame.display.update()

class171 = class171(20, 310, 64, 64, 450)

camera = Camera(500, 480)

run = True
while run:
    clock.tick(27)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.USEREVENT + 1:
            if class171.door_phase == 1:
                class171.door_phase = 2
                class171.door_timer = current_time + 15000
            elif class171.door_phase == 3:
                class171.door_phase = 0
                class171.movement_disabled = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_h] and current_time - class171.last_horn_time > 3000:
        class171.horn_sound.play()
        class171.last_horn_time = current_time
    if keys[pygame.K_t] and class171.vel == 0 and class171.door_phase == 0:
        class171.door_phase = 1
        class171.movement_disabled = True
        class171.sequence_start_time = current_time
        class171.door_channel.play(class171.door_open_sound)
        class171.door_channel.set_endevent(pygame.USEREVENT + 1)
    if class171.door_phase == 2 and current_time >= class171.door_timer:
        class171.door_phase = 3
        class171.door_channel.play(class171.door_close_sound)
        class171.door_channel.set_endevent(pygame.USEREVENT + 1)
    move_right = keys[pygame.K_w] or keys[pygame.K_UP]
    move_left = keys[pygame.K_s] or keys[pygame.K_DOWN]
    class171.move(move_right, move_left)
    camera.update(class171)
    print("Speed:", class171.vel * class171.acc, "mph")
    redrawGameWindow()


pygame.quit()