from static import Colours
import pygame


class ObstacleSprite(pygame.sprite.Sprite):
    def __init__(self, objType, coord, corners):
        super().__init__()
        self.type = objType
        self.x = coord[0]
        self.y = coord[1]
        self.corners = corners
        if self.type == "polygon":
            self.image = pygame.Surface((200, 150), pygame.SRCALPHA, 32)
            self.mask = pygame.mask.from_surface(self.image)
        elif self.type == "rect":
            self.width = corners[0]
            self.height = corners[1]
            self.image = pygame.Surface((corners[0], corners[1]))
            self.rect = self.image.fill(Colours.white)
        self.rect = self.image.get_rect()
        self.rect.topleft = coord

    def update(self):
        pass

    def drawObstacle(self, screen):
        if self.type == "rect":
            pygame.draw.rect(screen, Colours.darkGrey, [self.x + 30, self.y + 30, self.width - 60, self.height - 60])
            pygame.draw.rect(screen, Colours.black, [self.x, self.y, self.width, self.height], 3)
            pygame.draw.rect(screen, Colours.black, [self.x + 30, self.y + 30, self.width - 60, self.height - 60], 3)

            pygame.draw.line(screen, Colours.black, [self.x + 2, self.y + 2], [self.x + 30, self.y + 30], 3)
            pygame.draw.line(screen, Colours.black, [self.x + self.width - 2, self.y + 2], [self.x + self.width - 32, self.y + 32], 3)
            pygame.draw.line(screen, Colours.black, [self.x + 2, self.y + self.height - 2], [self.x + 32, self.y + self.height - 32], 3)
            pygame.draw.line(screen, Colours.black, [self.x + self.width - 2, self.y + self.height - 2], [self.x + self.width - 32, self.y + self.height - 32], 3)
        elif self.type == "polygon":
            pygame.draw.polygon(screen, Colours.white, self.corners)
