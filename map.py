import pygame
from shapely import geometry


class Wall:
    def __init__(self, corners):
        self.corners = corners
        self.polygon = geometry.Polygon(self.corners)
        self.distance = 0
        center = list(self.polygon.centroid.coords)[0]
        self.center = (int(center[0]), int(center[1]))


class Map:
    def __init__(self):
        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions)
        self.render_surface.set_colorkey('black')

        self.map_layout = [
            [(267, 224), (281, 292), (385, 289), (370, 214)],
            [(737, 509), (860, 510), (872, 587), (775, 632)],
            [(1609, 159), (1725, 145), (1738, 305), (1614, 314)]
        ]

        self.walls = []

        for polygon in self.map_layout:
            self.walls.append(Wall(polygon))
            pygame.draw.polygon(self.render_surface, 'grey', polygon)

    def draw_walls(self, surface):
        surface.blit(self.render_surface, (0, 0))
