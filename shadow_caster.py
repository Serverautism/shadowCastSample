import pygame
from shapely import geometry


class Shadow:
    def __init__(self, corners):
        self.corners = corners
        self.polygon = geometry.Polygon(self.corners)


class ShadowCaster:
    def __init__(self, map):
        self.map = map

        self.font = pygame.font.SysFont('Arial', 20, bold=True)

        self.colors = {
            'text': (53, 80, 112),
            'shadows': (109, 89, 122),
            'green': (42, 157, 143),
            'red': (229, 107, 111),
            'blue': (24, 29, 171)
        }

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.shadow_render_surface = pygame.Surface(self.render_dimensions)
        self.shadow_render_surface.set_colorkey('black')
        self.debug_render_surface = pygame.Surface(self.render_dimensions)
        self.debug_render_surface.set_colorkey('black')

        self.render_corners = [(0, 0), (self.render_width, 0), (self.render_width, self.render_height), (0, self.render_height)]
        self.render_polygon = geometry.Polygon(self.render_corners)

        self.last_player_center = [0, 0]

    def update(self, player_center):
        # check if player moved
        if self.last_player_center != player_center:
            self.last_player_center = player_center.copy()
            self.shadow_render_surface.fill('black')
            self.debug_render_surface.fill('black')

            # check distance from every wall to player
            for wall in self.map.walls:
                wall.distance = round(wall.polygon.distance(geometry.Point(player_center)), 2)

            wall_shadows = []
            skipped_walls = 0

            # handle every wall from nearest to furthest
            for i, wall in enumerate(sorted(self.map.walls, key=lambda x: x.distance)):
                # check if wall is covered by another shadow
                skip = False
                for j, finished_shadow in enumerate(wall_shadows):
                    if finished_shadow.polygon.contains(wall.polygon):
                        skip = True
                        self.debug_render_surface.blit(
                            self.font.render(str(j + 1 + skipped_walls), False, self.colors['text']),
                            (wall.center[0], wall.center[1] - 15))
                        break

                if skip:
                    continue

                allpoints = []
                new_points = []

                for corner in wall.corners:
                    # vector = [change in x direction, change in y direction]
                    vector_x = corner[0] - player_center[0]
                    vector_y = corner[1] - player_center[1]
                    vector_length = (vector_x ** 2 + vector_y ** 2) ** .5

                    # unit vector = vector with a total change of 1
                    unit_vector_x = vector_x / vector_length
                    unit_vector_y = vector_y / vector_length

                    if unit_vector_x < 0:
                        shadow_length_x = -corner[0] / unit_vector_x
                    elif unit_vector_x > 0:
                        shadow_length_x = (self.render_width - corner[0]) / unit_vector_x
                    else:
                        shadow_length_x = 1000

                    if unit_vector_y < 0:
                        shadow_length_y = -corner[1] / unit_vector_y
                    elif unit_vector_y > 0:
                        shadow_length_y = (self.render_height - corner[1]) / unit_vector_y
                    else:
                        shadow_length_y = 1000

                    shadow_length = min(shadow_length_x, shadow_length_y)

                    new_x = corner[0] + unit_vector_x * shadow_length
                    new_y = corner[1] + unit_vector_y * shadow_length

                    new_point = (int(new_x), int(new_y))

                    allpoints.append(corner)
                    allpoints.append(new_point)
                    new_points.append(new_point)

                    # draw debug stuff
                    pygame.draw.circle(self.debug_render_surface, self.colors['red'], corner, 4)
                    pygame.draw.circle(self.debug_render_surface, self.colors['green'], new_point, 4)
                    pygame.draw.line(self.debug_render_surface, self.colors['red'], player_center, corner)
                    pygame.draw.line(self.debug_render_surface, self.colors['green'], corner, new_point)

                for point in self.render_corners:
                    line = [player_center, point]
                    shapely_line = geometry.LineString(line)
                    if wall.polygon.intersects(shapely_line):
                        allpoints.append(point)

                shadow_polygon = list(geometry.MultiPoint(allpoints).convex_hull.exterior.coords)

                wall_shadows.append(Shadow(shadow_polygon))

                self.debug_render_surface.blit(
                    self.font.render(str(i+1), False, self.colors['text']), (wall.center[0], wall.center[1] - 15))
                self.debug_render_surface.blit(
                    self.font.render(str(wall.distance), False, self.colors['text']), wall.center)

                pygame.draw.polygon(self.shadow_render_surface, self.colors['shadows'], shadow_polygon)

    def draw_shadows(self, surface):
        surface.blit(self.shadow_render_surface, (0, 0))

    def draw_debug(self, surface):
        surface.blit(self.debug_render_surface, (0, 0))
