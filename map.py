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
            [(187, 175), (187, 214), (214, 211), (216, 173)],
            [(1006, 117), (1139, 175), (1021, 251)],
            [(451, 473), (473, 246), (636, 221), (715, 288), (762, 410), (581, 333)],
            [(1140, 512), (1216, 482), (1434, 540), (1545, 659), (1538, 814), (1476, 909), (1180, 992), (1036, 919), (1086, 776), (1162, 781), (1229, 827), (1293, 848), (1347, 803), (1390, 685), (1296, 600), (1177, 598), (1136, 666), (1043, 652), (1027, 554)],
            [(122, 670), (124, 1012), (758, 998), (733, 658), (212, 669), (214, 706), (685, 711), (705, 956), (176, 975), (171, 673)]
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
