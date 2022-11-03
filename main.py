import pygame
from map import Map
from shadow_caster import ShadowCaster


class Game:
    def __init__(self):
        pygame.init()

        # drawing related stuff
        self.running = True

        self.font = pygame.font.SysFont('Arial', 20)

        self.fps = 120
        self.clock = pygame.time.Clock()

        self.screen_width, self.screen_height = 1920, 1080
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        self.render_width, self.render_height = 1920, 1080
        self.render_dimensions = (self.render_width, self.render_height)
        self.render_surface = pygame.Surface(self.render_dimensions).convert_alpha()

        # player related
        self.player_position = [1920/2, 1080/2]
        self.player_speed = 2

        # other objects
        self.map = Map()
        self.shadow_caster = ShadowCaster(self.map)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            # draw map
            self.shadow_caster.update([self.player_position[0], self.player_position[1]], self.render_surface)
            self.map.update(self.render_surface)
            
            # draw player position
            pygame.draw.circle(self.render_surface, 'red', self.player_position, 10)

            self.render_surface.blit(self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, 'darkgrey'), (5, 5))
            self.screen.blit(pygame.transform.scale(self.render_surface, self.screen_dimensions), (0, 0))
            pygame.display.update()
            self.render_surface.fill('black')

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_w]:
            self.player_position[1] -= self.player_speed
        if pressed_keys[pygame.K_a]:
            self.player_position[0] -= self.player_speed
        if pressed_keys[pygame.K_s]:
            self.player_position[1] += self.player_speed
        if pressed_keys[pygame.K_d]:
            self.player_position[0] += self.player_speed


if __name__ == '__main__':
    app = Game()
    app.run()
