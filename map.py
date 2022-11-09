import pygame
from shapely import geometry, ops


class Wall:
    def __init__(self, corners, polygon):
        self.corners = corners
        self.polygon = polygon
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
            [(127, 99), (130, 812), (185, 811), (166, 100)],
            [(212, 101), (525, 114), (607, 271), (557, 522), (246, 561), (238, 517), (520, 482), (565, 281), (509, 152), (211, 134)],
            [(737, 124), (782, 121), (1004, 551), (984, 586)],
            [(957, 852), (1013, 852), (1295, 111), (1224, 104)],
            [(1458, 819), (1455, 854), (1493, 854), (1495, 821)]
        ]

        self.walls = []
        self.new_walls = []

        for corners in self.map_layout:
            # make the polygon clockwise
            edge_values = []
            for i in range(-1, len(corners) - 1):
                value = (corners[i + 1][0] - corners[i][0]) * (corners[i + 1][1] + corners[i][1])
                edge_values.append(value)
            solution = sum(edge_values)

            if solution > 0:
                corners.reverse()

            # draw to screen
            pygame.draw.polygon(self.render_surface, self.colors['walls'], corners)

            # make shapely polygon
            polygon = geometry.Polygon(corners)

            # check for indents
            convex_hull_area = geometry.MultiPoint(corners).convex_hull.area
            polygon_area = polygon.area

            if convex_hull_area != polygon_area:
                triangles = ops.triangulate(polygon)

                for t in triangles:
                    if polygon.contains(t):
                        self.new_walls.append(t)
                continue

            self.walls.append(Wall(corners, polygon))

        for triangle in self.new_walls:
            corners = triangle.exterior.coords
            self.walls.append(Wall(corners, triangle))

    def draw_walls(self, surface):
        surface.blit(self.render_surface, (0, 0))
