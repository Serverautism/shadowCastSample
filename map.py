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
            [(718, 258), (868, 171), (1117, 173), (1247, 256), (1270, 418), (1201, 554), (1005, 640), (812, 657), (902, 556), (1022, 518), (1100, 443), (1107, 369), (1059, 320), (968, 305), (890, 322), (833, 385), (794, 450), (693, 382)]
        ]

        self.walls = []

        for polygon in self.map_layout:
            self.walls.append(Wall(polygon))
            pygame.draw.polygon(self.render_surface, 'grey', polygon)

    def draw_walls(self, surface):
        surface.blit(self.render_surface, (0, 0))
