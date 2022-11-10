import pygame
from shapely import geometry, ops


class Shadow:
    def __init__(self, polygon, corners):
        self.polygon = polygon
        self.corners = corners


class ShadowCaster:
    def __init__(self, map):
        self.map = map

        self.font = pygame.font.SysFont('Arial', 20, bold=True)

        self.colors = {
            'text': (38, 70, 83),
            'shadows': (38, 70, 83),
            'green': (42, 157, 143),
            'red': (229, 107, 111)
        }

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.shadow_render_surface = pygame.Surface(self.render_dimensions)
        self.shadow_render_surface.set_colorkey('black')
        self.debug_render_surface = pygame.Surface(self.render_dimensions)
        self.debug_render_surface.set_colorkey('black')

        self.render_corners = [(0, 0), (self.render_width, 0), (self.render_width, self.render_height), (0, self.render_height)]
        self.render_polygon = geometry.Polygon(self.render_corners)

        self.obstacle_shadows = []
        self.shaded_areas = []
        self.shaded_obstacles = []
        self.visible_obstacles = []
        self.rays = []

    def generate_shadows(self, source):
        self.obstacle_shadows.clear()
        self.shaded_areas.clear()
        self.shaded_obstacles.clear()
        self.visible_obstacles.clear()
        self.rays.clear()

        # check distance from every obstacle to player
        for obstacle in self.map.obstacles:
            obstacle.distance = round(obstacle.polygon.distance(geometry.Point(source)), 2)

        # handle every obstacle from nearest to furthest
        for i, obstacle in enumerate(sorted(self.map.obstacles, key=lambda x: x.distance)):
            # check if obstacle is already covered by a shadow
            skip = False
            for j, shadow in enumerate(self.obstacle_shadows):
                if shadow.polygon.contains(obstacle.polygon):
                    skip = True
                    self.shaded_obstacles.append((obstacle, j + 1))
                    break

            if skip:
                continue

            self.visible_obstacles.append((obstacle, i + 1))

            allpoints = []

            for corner in obstacle.corners:
                # vector = [change in x direction, change in y direction]
                vector_x = corner[0] - source[0]
                vector_y = corner[1] - source[1]
                vector_length = (vector_x ** 2 + vector_y ** 2) ** .5

                # unit vector = vector with a total change of 1
                unit_vector_x = vector_x / vector_length
                unit_vector_y = vector_y / vector_length

                if unit_vector_x < 0:
                    shadow_length_x = -corner[0] / unit_vector_x
                elif unit_vector_x > 0:
                    shadow_length_x = (self.render_width - corner[0]) / unit_vector_x
                else:
                    shadow_length_x = self.render_width

                if unit_vector_y < 0:
                    shadow_length_y = -corner[1] / unit_vector_y
                elif unit_vector_y > 0:
                    shadow_length_y = (self.render_height - corner[1]) / unit_vector_y
                else:
                    shadow_length_y = self.render_width

                shadow_length = min(shadow_length_x, shadow_length_y)

                new_x = corner[0] + unit_vector_x * shadow_length
                new_y = corner[1] + unit_vector_y * shadow_length

                new_point = (int(new_x), int(new_y))

                allpoints.append(corner)
                allpoints.append(new_point)

                self.rays.append((source, corner, new_point))

            for point in self.render_corners:
                line = [source, point]
                shapely_line = geometry.LineString(line)
                if obstacle.polygon.intersects(shapely_line):
                    allpoints.append(point)

            shadow_polygon = geometry.MultiPoint(allpoints).convex_hull
            shadow_corners = list(shadow_polygon.exterior.coords)

            self.obstacle_shadows.append(Shadow(shadow_polygon, shadow_corners))

        render_shapes = ops.unary_union([s.polygon for s in self.obstacle_shadows])
        if type(render_shapes) == geometry.MultiPolygon:
            if len(render_shapes.geoms) < len(self.obstacle_shadows):
                for polygon in render_shapes.geoms:
                    corners = list(polygon.exterior.coords)
                    self.shaded_areas.append(Shadow(polygon, corners))
            else:
                for obstacle, shadow in zip(self.visible_obstacles, self.obstacle_shadows):
                    shadow.polygon = shadow.polygon.difference(obstacle[0].polygon)
                    shadow.corners = list(shadow.polygon.exterior.coords)
                    self.shaded_areas = self.obstacle_shadows
        else:
            if len(list(render_shapes.interiors)) == 0:
                corners = list(render_shapes.exterior.coords)
                self.shaded_areas.append(Shadow(render_shapes, corners))
            elif len(list(render_shapes.interiors)) == 1:
                corners = list(render_shapes.exterior.coords)
                interior_coords = list(render_shapes.interiors[0].coords)
                interior_polygon = geometry.Polygon(interior_coords)
                interior_coords.reverse()

                check = False
                connection_index = 0
                for i, point in enumerate(corners):
                    if type(interior_polygon.intersection(geometry.LineString([interior_coords[0], point]))) == geometry.Point:
                        check = True
                        connection_index = i
                        corners.pop(-1)
                        break
                if not check:
                    print('Keine Lösung gefunden...')

                corners = corners[connection_index:] + corners[:connection_index]
                corners.append(corners[0])

                corners += interior_coords
                self.shaded_areas.append(Shadow(geometry.Polygon(corners), corners))
            else:
                print('ERROR shadow has more than two holes')

    def render_shadows(self):
        self.shadow_render_surface.fill('black')
        for shadow in self.shaded_areas:
            pygame.draw.polygon(self.shadow_render_surface, self.colors['shadows'], shadow.corners)
        return self.shadow_render_surface

    def render_debug(self):
        self.debug_render_surface.fill('black')
        for obstacle, number in self.shaded_obstacles:
            self.debug_render_surface.blit(self.font.render(str(number), False, self.colors['text']), (obstacle.center[0], obstacle.center[1] - 15))

        for obstacle, number in self.visible_obstacles:
            self.debug_render_surface.blit(self.font.render(str(number), False, self.colors['text']), (obstacle.center[0], obstacle.center[1] - 15))
            self.debug_render_surface.blit(self.font.render(str(obstacle.distance), False, self.colors['text']), obstacle.center)

        for source, corner, new_point in self.rays:
            pygame.draw.circle(self.debug_render_surface, self.colors['red'], corner, 4)
            pygame.draw.circle(self.debug_render_surface, self.colors['green'], new_point, 4)
            pygame.draw.line(self.debug_render_surface, self.colors['red'], source, corner)
            pygame.draw.line(self.debug_render_surface, self.colors['green'], corner, new_point)

    def draw_shadows(self, surface):
        surface.blit(self.shadow_render_surface, (0, 0))

    def draw_debug(self, surface):
        surface.blit(self.debug_render_surface, (0, 0))
