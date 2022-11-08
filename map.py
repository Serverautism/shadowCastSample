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
        self.colors = {
            'walls': (181, 101, 118)
        }

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions)
        self.render_surface.set_colorkey('black')

        self.map_layout = [
            [(388, 398), (480, 186), (864, 253), (724, 495)],
            [(342, 844), (391, 777), (503, 823), (419, 889)],
            [(978, 713), (1292, 571), (1400, 973)],
            [(1399, 168), (1702, 95), (1685, 229), (1554, 243)],
            [(1078, 410), (1102, 239), (1329, 303)],
            [(1691, 636), (1845, 733), (1686, 855), (1548, 723)],
            [(277, 613), (380, 557), (692, 591), (707, 624)],
            [(193, 90), (85, 559), (158, 567), (407, 49)]
        ]

        self.walls = []

        for polygon in self.map_layout:
            self.walls.append(Wall(polygon))
            pygame.draw.polygon(self.render_surface, self.colors['walls'], polygon)

    def draw_walls(self, surface):
        surface.blit(self.render_surface, (0, 0))
