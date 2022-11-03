import pygame
from shapely import geometry


class Wall:
    def __init__(self, corners):
        self.corners = corners
        self.polygon = geometry.Polygon(self.corners)
        self.distance = 0


class Map:
    def __init__(self):
        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions).convert_alpha()
        self.render_surface.set_colorkey('black')

        self.map_layout = [
            [[100, 100], [175, 100], [175, 175], [100, 175]],
            [[275, 100], [350, 100], [350, 175], [275, 175]],
            [[450, 100], [525, 100], [525, 175], [450, 175]],
            [[625, 100], [700, 100], [700, 175], [625, 175]],
            [[800, 100], [875, 100], [875, 175], [800, 175]],
            [[975, 100], [1050, 100], [1050, 175], [975, 175]],
            [[1150, 100], [1225, 100], [1225, 175], [1150, 175]],
            [[1325, 100], [1400, 100], [1400, 175], [1325, 175]],
            [[1500, 100], [1575, 100], [1575, 175], [1500, 175]],
            [[1675, 100], [1750, 100], [1750, 175], [1675, 175]],
            [[100, 275], [175, 275], [175, 350], [100, 350]],
            [[275, 275], [350, 275], [350, 350], [275, 350]],
            [[450, 275], [525, 275], [525, 350], [450, 350]],
            [[625, 275], [700, 275], [700, 350], [625, 350]],
            [[800, 275], [875, 275], [875, 350], [800, 350]],
            [[975, 275], [1050, 275], [1050, 350], [975, 350]],
            [[1150, 275], [1225, 275], [1225, 350], [1150, 350]],
            [[1325, 275], [1400, 275], [1400, 350], [1325, 350]],
            [[1500, 275], [1575, 275], [1575, 350], [1500, 350]],
            [[1675, 275], [1750, 275], [1750, 350], [1675, 350]],
            [[100, 450], [175, 450], [175, 525], [100, 525]],
            [[275, 450], [350, 450], [350, 525], [275, 525]],
            [[450, 450], [525, 450], [525, 525], [450, 525]],
            [[625, 450], [700, 450], [700, 525], [625, 525]],
            [[800, 450], [875, 450], [875, 525], [800, 525]],
            [[975, 450], [1050, 450], [1050, 525], [975, 525]],
            [[1150, 450], [1225, 450], [1225, 525], [1150, 525]],
            [[1325, 450], [1400, 450], [1400, 525], [1325, 525]],
            [[1500, 450], [1575, 450], [1575, 525], [1500, 525]],
            [[1675, 450], [1750, 450], [1750, 525], [1675, 525]],
            [[100, 625], [175, 625], [175, 700], [100, 700]],
            [[275, 625], [350, 625], [350, 700], [275, 700]],
            [[450, 625], [525, 625], [525, 700], [450, 700]],
            [[625, 625], [700, 625], [700, 700], [625, 700]],
            [[800, 625], [875, 625], [875, 700], [800, 700]],
            [[975, 625], [1050, 625], [1050, 700], [975, 700]],
            [[1150, 625], [1225, 625], [1225, 700], [1150, 700]],
            [[1325, 625], [1400, 625], [1400, 700], [1325, 700]],
            [[1500, 625], [1575, 625], [1575, 700], [1500, 700]],
            [[1675, 625], [1750, 625], [1750, 700], [1675, 700]],
            [[100, 800], [175, 800], [175, 875], [100, 875]],
            [[275, 800], [350, 800], [350, 875], [275, 875]],
            [[450, 800], [525, 800], [525, 875], [450, 875]],
            [[625, 800], [700, 800], [700, 875], [625, 875]],
            [[800, 800], [875, 800], [875, 875], [800, 875]],
            [[975, 800], [1050, 800], [1050, 875], [975, 875]],
            [[1150, 800], [1225, 800], [1225, 875], [1150, 875]],
            [[1325, 800], [1400, 800], [1400, 875], [1325, 875]],
            [[1500, 800], [1575, 800], [1575, 875], [1500, 875]],
            [[1675, 800], [1750, 800], [1750, 875], [1675, 875]],
            [[100, 975], [175, 975], [175, 1050], [100, 1050]],
            [[275, 975], [350, 975], [350, 1050], [275, 1050]],
            [[450, 975], [525, 975], [525, 1050], [450, 1050]],
            [[625, 975], [700, 975], [700, 1050], [625, 1050]],
            [[800, 975], [875, 975], [875, 1050], [800, 1050]],
            [[975, 975], [1050, 975], [1050, 1050], [975, 1050]],
            [[1150, 975], [1225, 975], [1225, 1050], [1150, 1050]],
            [[1325, 975], [1400, 975], [1400, 1050], [1325, 1050]],
            [[1500, 975], [1575, 975], [1575, 1050], [1500, 1050]],
            [[1675, 975], [1750, 975], [1750, 1050], [1675, 1050]]
        ]

        self.walls = []

        for polygon in self.map_layout:
            self.walls.append(Wall(polygon))
            pygame.draw.polygon(self.render_surface, 'grey', polygon)

    def update(self, surface):
        surface.blit(self.render_surface, (0, 0))
