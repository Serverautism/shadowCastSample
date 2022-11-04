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
            [[100, 100], [500, 100], [500, 120], [100, 120]],
            [[600, 100], [1000, 100], [1000, 120], [600, 120]],
            [[1100, 100], [1500, 100], [1500, 120], [1100, 120]],
            [[100, 220], [500, 220], [500, 240], [100, 240]],
            [[600, 220], [1000, 220], [1000, 240], [600, 240]],
            [[1100, 220], [1500, 220], [1500, 240], [1100, 240]],
            [[100, 340], [500, 340], [500, 360], [100, 360]],
            [[600, 340], [1000, 340], [1000, 360], [600, 360]],
            [[1100, 340], [1500, 340], [1500, 360], [1100, 360]],
            [[100, 460], [500, 460], [500, 480], [100, 480]],
            [[600, 460], [1000, 460], [1000, 480], [600, 480]],
            [[1100, 460], [1500, 460], [1500, 480], [1100, 480]],
            [[100, 580], [500, 580], [500, 600], [100, 600]],
            [[600, 580], [1000, 580], [1000, 600], [600, 600]],
            [[1100, 580], [1500, 580], [1500, 600], [1100, 600]],
            [[100, 700], [500, 700], [500, 720], [100, 720]],
            [[600, 700], [1000, 700], [1000, 720], [600, 720]],
            [[1100, 700], [1500, 700], [1500, 720], [1100, 720]],
            [[100, 820], [500, 820], [500, 840], [100, 840]],
            [[600, 820], [1000, 820], [1000, 840], [600, 840]],
            [[1100, 820], [1500, 820], [1500, 840], [1100, 840]],
            [[100, 940], [500, 940], [500, 960], [100, 960]],
            [[600, 940], [1000, 940], [1000, 960], [600, 960]],
            [[1100, 940], [1500, 940], [1500, 960], [1100, 960]]
        ]

        self.walls = []

        for polygon in self.map_layout:
            self.walls.append(Wall(polygon))
            pygame.draw.polygon(self.render_surface, 'grey', polygon)

    def draw_walls(self, surface):
        surface.blit(self.render_surface, (0, 0))
