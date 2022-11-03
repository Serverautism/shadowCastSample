import pygame
from shapely import geometry, ops


class Shadow:
    def __init__(self, corners):
        self.corners = corners
        self.polygon = geometry.Polygon(self.corners)


class ShadowCaster:
    def __init__(self, map):
        self.map = map

        self.colors = {
            'shadows': (83, 84, 84),
            'green': (2, 117, 2),
            'red': (133, 16, 16),
            'blue': (24, 29, 171)
        }

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions).convert_alpha()
        self.render_surface.set_colorkey('black')

        self.last_player_center = [0, 0]

    def update(self, player_center, debug=False):
        if self.last_player_center != player_center:
            self.last_player_center = player_center
            self.render_surface.fill('black')

            for wall in self.map.walls:
                nearest_point = list(ops.nearest_points(geometry.Point(player_center), wall.shapely)[1].coords)[0]
                wall.distance = round(((nearest_point[0] - player_center[0]) ** 2 + (nearest_point[1] - player_center[1]) ** 2) ** .5, 2)

            wall_shadows = []

            for wall in sorted(self.map.walls, key=lambda x: x.distance):
                allpoints = []

                new_points = []

                skip = False
                for finished_shadow in wall_shadows:
                    if finished_shadow.polygon.contains(wall.polygon):
                        skip = True
                        break

                if skip:
                    continue

                for corner in wall.corners:
                    # vector = [change in x direction, change in y direction]
                    vector_x = corner[0] - player_center[0]
                    vector_y = corner[1] - player_center[1]
                    vector = [vector_x, vector_y]

                    # unit vector = vector with a total change of 1
                    unit_vector_x = vector_x / (vector_x ** 2 + vector_y ** 2) ** .5
                    unit_vector_y = vector_y / (vector_x ** 2 + vector_y ** 2) ** .5
                    unit_vector = [unit_vector_x, unit_vector_y]

                    if unit_vector_x < 0:
                        shadow_length_x = (0 - corner[0]) / unit_vector_x
                    elif unit_vector_x > 0:
                        shadow_length_x = (self.render_width - corner[0]) / unit_vector_x
                    else:
                        shadow_length_x = 10 ** 10

                    if unit_vector_y < 0:
                        shadow_length_y = (0 - corner[1]) / unit_vector_y
                    elif unit_vector_y > 0:
                        shadow_length_y = (self.render_height - corner[1]) / unit_vector_y
                    else:
                        shadow_length_y = 10 ** 10

                    shadow_length = min(shadow_length_x, shadow_length_y)

                    new_x = corner[0] + unit_vector_x * shadow_length
                    new_y = corner[1] + unit_vector_y * shadow_length

                    new_point = [int(new_x), int(new_y)]

                    allpoints.append(corner)
                    allpoints.append(new_point)
                    new_points.append(new_point)
                    
                    if debug:
                        pygame.draw.circle(self.render_surface, self.colors['red'], corner, 2)
                        pygame.draw.circle(self.render_surface, self.colors['green'], new_point, 2)

                        pygame.draw.aaline(self.render_surface, self.colors['red'], player_center, corner)
                        pygame.draw.aaline(self.render_surface, self.colors['green'], corner, new_point)