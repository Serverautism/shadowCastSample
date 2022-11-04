import pygame
from shapely import geometry, ops
from scipy import spatial
from threading import Thread


class Shadow:
    def __init__(self, corners):
        self.corners = corners
        self.polygon = geometry.Polygon(self.corners)


class ShadowCaster:
    def __init__(self, map):
        self.map = map

        self.font = pygame.font.SysFont('Arial', 20)

        self.colors = {
            'text': (5, 5, 5),
            'shadows': (83, 84, 84),
            'green': (32, 252, 3),
            'red': (133, 16, 16),
            'blue': (24, 29, 171)
        }

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.shadow_render_surface = pygame.Surface(self.render_dimensions)
        self.shadow_render_surface.set_colorkey('black')
        self.debug_render_surface = pygame.Surface(self.render_dimensions)
        self.debug_render_surface.set_colorkey('black')

        self.last_player_center = [0, 0]

    def update(self, player_center, debug=False):
        if self.last_player_center != player_center:
            self.last_player_center = player_center.copy()
            self.shadow_render_surface.fill('black')

            if debug:
                self.debug_render_surface.fill('black')

            for wall in self.map.walls:
                nearest_point = list(ops.nearest_points(geometry.Point(player_center), wall.polygon)[1].coords)[0]
                wall.distance = round(((nearest_point[0] - player_center[0]) ** 2 + (nearest_point[1] - player_center[1]) ** 2) ** .5, 2)

            wall_shadows = []
            skipped_walls = 0

            for i, wall in enumerate(sorted(self.map.walls, key=lambda x: x.distance)):
                allpoints = []

                new_points = []

                skip = False
                for j, finished_shadow in enumerate(wall_shadows):
                    if finished_shadow.polygon.contains(wall.polygon):
                        skip = True
                        if debug:
                            self.debug_render_surface.blit(
                                self.font.render(str(j + 1 + skipped_walls), True, self.colors['text']),
                                (wall.center[0], wall.center[1] - 15))
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
                        pygame.draw.circle(self.debug_render_surface, self.colors['red'], corner, 4)
                        pygame.draw.circle(self.debug_render_surface, self.colors['green'], new_point, 4)

                        pygame.draw.aaline(self.debug_render_surface, self.colors['red'], player_center, corner)
                        pygame.draw.aaline(self.debug_render_surface, self.colors['green'], corner, new_point)

                new_x_values = [i[0] for i in new_points]
                new_y_values = [i[1] for i in new_points]
                left = 0 in new_x_values
                right = self.render_width in new_x_values
                top = 0 in new_y_values
                bottom = self.render_height in new_y_values

                if left and top:
                    allpoints.append([0, 0])

                if right and top:
                    allpoints.append([self.render_width, 0])

                if left and bottom:
                    allpoints.append([0, self.render_height])

                if right and bottom:
                    allpoints.append([self.render_width, self.render_height])

                if left and right and not top and not bottom:
                    wall_y_values = [i[1] for i in wall.corners]
                    if player_center[1] > max(wall_y_values):
                        allpoints.append([0, 0])
                        allpoints.append([self.render_width, 0])

                    if player_center[1] < min(wall_y_values):
                        allpoints.append([0, self.render_height])
                        allpoints.append([self.render_width, self.render_height])

                if top and bottom and not left and not right:
                    wall_x_values = [i[0] for i in wall.corners]
                    if player_center[0] > max(wall_x_values):
                        allpoints.append([0, 0])
                        allpoints.append([0, self.render_height])

                    if player_center[0] < min(wall_x_values):
                        allpoints.append([self.render_width, 0])
                        allpoints.append([self.render_width, self.render_height])

                '''shadow_indices = spatial.ConvexHull(allpoints).vertices
                shadow_polygon = [allpoints[i] for i in shadow_indices]'''

                shadow_polygon = list(geometry.MultiPoint(allpoints).convex_hull.exterior.coords)

                wall_shadows.append(Shadow(shadow_polygon))

                if debug:
                    self.debug_render_surface.blit(
                        self.font.render(str(i+1), True, self.colors['red']), (wall.center[0], wall.center[1] - 15))
                    self.debug_render_surface.blit(
                        self.font.render(str(wall.distance), True, self.colors['text']), wall.center)

                pygame.draw.polygon(self.shadow_render_surface, self.colors['shadows'], shadow_polygon)

    def draw_shadows(self, surface):
        surface.blit(self.shadow_render_surface, (0, 0))

    def draw_debug(self, surface):
        surface.blit(self.debug_render_surface, (0, 0))
