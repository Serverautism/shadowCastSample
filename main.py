import pygame
from map import Map
from shadow_caster import ShadowCaster


class Game:
    def __init__(self):
        pygame.init()

        self.running = True
        self.debug = False

        # drawing related stuff
        self.colors = {
            'text': (231, 111, 81),
            'background': (233, 196, 106),
            'player': (244, 162, 97)
        }

        self.font = pygame.font.SysFont('Arial', 20)

        self.fps = 120
        self.clock = pygame.time.Clock()

        self.screen_width, self.screen_height = 1920, 1080
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions)

        # player related
        self.player_position = [1920 / 2, 1080 / 2]
        self.player_speed = 2

        # other objects
        self.map = Map()
        self.shadow_caster = ShadowCaster(self.map)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            # draw map
            self.shadow_caster.generate_shadows(self.player_position)
            self.shadow_caster.render_shadows()
            self.shadow_caster.render_debug()
            self.shadow_caster.draw_shadows(self.render_surface)
            self.map.draw_obstacles(self.render_surface)

            if self.debug:
                self.shadow_caster.draw_debug(self.render_surface)

            # draw player position
            pygame.draw.circle(self.render_surface, self.colors['player'], self.player_position, 8)

            self.render_surface.blit(self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, self.colors['text']), (5, 5))
            self.screen.blit(pygame.transform.scale(self.render_surface, self.screen_dimensions), (0, 0))
            pygame.display.update()
            self.render_surface.fill(self.colors['background'])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_f:
                    if self.debug:
                        self.debug = False
                    else:
                        self.debug = True

        if pygame.mouse.get_pressed()[0]:
            self.player_position = pygame.mouse.get_pos()


if __name__ == '__main__':
    app = Game()
    app.run()
