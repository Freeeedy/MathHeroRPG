import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self ,frame, row, width, height, color):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0,0), (frame * width, row * height, width, height))
        image.set_colorkey(color)
        return image 