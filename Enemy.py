import pygame

from SpriteSheet import SpriteSheet


class Enemy:

    def __init__(self, name, idle_path, hit_path, death_path, x, y, max_hp, damage, damage_sound, scale=1):
        self.x = x
        self.y = y

        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.damage = damage

        self.scale = scale

        # Idle
        self.idle_frames = self.load_frames(idle_path, 7)

        # Hit
        self.hit_frames = self.load_frames(hit_path, 5)

        # Death
        self.death_frames = self.load_frames(death_path, 15)

        # Animation
        self.animation = self.idle_frames
        self.animation_type = "idle"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 120

        self.image = self.animation[0]
        self.rect = self.image.get_rect(center=(x, y))

        self.damage_sound = damage_sound

        self.dead = False

    def load_frames(self, path, frame_count):
        sheet = pygame.image.load(path).convert_alpha()
        sprite_sheet = SpriteSheet(sheet)

        frames = []

        for frame in range(frame_count):
            image = sprite_sheet.get_image(frame, 0, 80, 64, (0, 0, 0))

            if self.scale != 1:
                image = pygame.transform.scale(
                    image,
                    (80 * self.scale, 64 * self.scale)
                )

            frames.append(image)

        return frames

    def update(self, dt):
        self.animation_timer += dt

        if self.animation_timer < self.animation_speed:
            return

        self.animation_timer = 0
        self.current_frame += 1

        # Death animation
        if self.animation_type == "death":
            if self.current_frame >= len(self.animation):
                self.current_frame = len(self.animation) - 1
                self.dead = True

            self.image = self.animation[self.current_frame]
            return

        # Hit animation
        if self.animation_type == "hit":
            if self.current_frame >= len(self.animation):
                self.animation = self.idle_frames
                self.animation_type = "idle"
                self.current_frame = 0

            self.image = self.animation[self.current_frame]
            return

        # Idle animation
        if self.current_frame >= len(self.animation):
            self.current_frame = 0

        self.image = self.animation[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        if self.dead or self.animation_type == "death":
            return

        self.damage_sound.play()

        self.hp = max(0, self.hp - amount)

        if self.hp <= 0:
            self.animation = self.death_frames
            self.animation_type = "death"
            self.current_frame = 0
            self.animation_timer = 0
            self.image = self.animation[0]

        else:
            self.animation = self.hit_frames
            self.animation_type = "hit"
            self.current_frame = 0
            self.animation_timer = 0
            self.image = self.animation[0]

    def is_dead(self):
        return self.dead