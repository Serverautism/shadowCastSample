import pygame
from shapely import geometry, ops


class Obstacle:
    def __init__(self, corners, polygon):
        self.corners = corners
        self.polygon = polygon
        self.distance = 0
        center = list(self.polygon.centroid.coords)[0]
        self.center = (int(center[0]), int(center[1]))


class Map:
    def __init__(self):
        self.colors = {
            'obstacles': (42, 157, 143)
        }

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions)
        self.render_surface.set_colorkey('black')

        self.map_layout = [
            [(220, 396), (193, 505), (322, 517), (347, 397)],
            [(548, 681), (568, 610), (670, 710)],
            [(806, 417), (922, 310), (866, 103), (547, 190)],
            [(1131, 725), (1194, 582), (1318, 549), (1579, 747)],
            [(1318, 140), (1556, 133), (1673, 230)],
            [(910, 907), (1066, 919), (1006, 968)],
            [(759, 1049), (760, 1029), (796, 1028), (799, 1046)]
        ]

        self.obstacles = []
        self.new_obstacles = []

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
            pygame.draw.polygon(self.render_surface, self.colors['obstacles'], corners)

            # make shapely polygon
            polygon = geometry.Polygon(corners)

            # check for indents
            convex_hull_area = geometry.MultiPoint(corners).convex_hull.area
            polygon_area = polygon.area

            if convex_hull_area != polygon_area:
                triangles = ops.triangulate(polygon)

                for t in triangles:
                    if polygon.contains(t):
                        self.new_obstacles.append(t)
                continue

            self.obstacles.append(Obstacle(corners, polygon))

        for triangle in self.new_obstacles:
            corners = list(triangle.exterior.coords)
            self.obstacles.append(Obstacle(corners, triangle))

    def draw_obstacles(self, surface):
        surface.blit(self.render_surface, (0, 0))
