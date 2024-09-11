import pygame
import random
from statistics import mean

screen_width, screen_height = 800, 600  # 0, 0 for fullscreen
MARGIN = screen_width * 0.1


class Boid:
    NUM_BOIDS = 100
    DISTANCE_VISIBLE = 42
    DISTANCE_SEPERATION = 20
    MAX_SPEED = 0.5
    COHERENCE_FACTOR  = 0.0001
    ALIGNMENT_FACTOR  = 0.008
    SEPARATION_FACTOR = 0.001
    
    def __init__(self, color=(0,255,255)):
        self.position = pygame.math.Vector2(random.randint(0, screen_width), random.randint(0, screen_height))
        self.velocity = pygame.math.Vector2(random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED), random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED))
        self.velocity_buffer = self.velocity.copy()
        self.color = color
    
    # Find the center of mass of the visible boids and slightly adjust velocity (`velocity_buffer`)
        # to point more towards the center of mass.
        # You will need `position` of each boid.
        # Use `Boid.COHERENCE_FACTOR` to control how much each boid "wants" to go towards that center.
    def cohere(self, boids):
        if len(boids)>0:
            c_o_mass = pygame.math.Vector2(mean([boid.position.x for boid in boids]),
                                           mean([boid.position.y for boid in boids]))

            self.velocity_buffer.x += (1 if (c_o_mass.x - self.position.x) > 0 else -1) * Boid.COHERENCE_FACTOR
            self.velocity_buffer.y += (1 if (c_o_mass.y - self.position.y) > 0 else -1) * Boid.COHERENCE_FACTOR
    
    # Find the average velocity (speed and direction) of the visible boids and
        # slightly adjust velocity (`velocity_buffer`) to match.
        # You will need `velocity` of each boid.
        # Use `Boid.ALIGNMENT_FACTOR` to control how much each boid "wants" to go in the same direction and speed as the visible boids.
    def align(self, boids):
        if len(boids) > 0:
            c_o_velocity = pygame.math.Vector2(mean([boid.velocity_buffer.x for boid in boids]),
                                               mean([boid.velocity_buffer.y for boid in boids]))

            self.velocity_buffer.x += (1 if (c_o_velocity.y - self.velocity_buffer.y) > 0 else -1) * Boid.ALIGNMENT_FACTOR
            self.velocity_buffer.y += (1 if (c_o_velocity.y - self.velocity_buffer.y) > 0 else -1) * Boid.ALIGNMENT_FACTOR

    # Move away from other visible boids that are too close (to avoid colliding)
        # by slightly adjusting velocity (`velocity_buffer`).
        # You will need `position` of each boid.
        # Use `Boid.SEPARATION_FACTOR` to control how much each boid "wants" to go away from neighboring boids.
        # Hint: opposite of `cohere()`
    def seperate(self, boids):
        if len(boids) > 0:
            c_o_mass = pygame.math.Vector2(mean([boid.position.x for boid in boids]),
                                           mean([boid.position.y for boid in boids]))

            self.velocity_buffer.x += (1 if (c_o_mass.x - self.position.x) < 0 else -1) * Boid.SEPARATION_FACTOR
            self.velocity_buffer.y += (1 if (c_o_mass.y - self.position.y) < 0 else -1) * Boid.SEPARATION_FACTOR
    
    def keep_in_bounds(self):
        TURN_FACTOR = 0.01
        turn = Boid.MAX_SPEED * TURN_FACTOR
        if self.position.x < MARGIN:
            self.velocity_buffer.x += turn
        if self.position.x > screen_width - MARGIN:
            self.velocity_buffer.x -= turn
        if self.position.y < MARGIN:
            self.velocity_buffer.y += turn
        if self.position.y > screen_height - MARGIN:
            self.velocity_buffer.y -= turn
    
    def update_position(self):
        if self.velocity_buffer.length() > Boid.MAX_SPEED:
            self.velocity_buffer *= 0.9
        self.velocity = self.velocity_buffer.copy()
        self.position += self.velocity


def main():
    global screen_width, screen_height
    pygame.init()
    screen = None
    if screen_width and screen_height:
        screen = pygame.display.set_mode((screen_width, screen_height))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h
    
    color_range = {"a": 50, "b": 255}
    boids = [Boid((random.randint(**color_range),
                   random.randint(**color_range),
                   random.randint(**color_range))) for _ in range(Boid.NUM_BOIDS)]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # background color
        screen.fill((0,0,0))

        for boid in boids:

            #### YOUR CODE HERE ####
            
            visible_boids = [bo for bo in boids if bo != boid
                             and abs(bo.position.x - boid.position.x) < Boid.DISTANCE_VISIBLE
                             and abs(bo.position.y - boid.position.y) < Boid.DISTANCE_VISIBLE
                             ]
            close_boids = []
            far_visible_boids = []

            for bo in visible_boids:
                if abs(bo.position.x - boid.position.x) < Boid.DISTANCE_SEPERATION and \
                   abs(bo.position.y - boid.position.y) < Boid.DISTANCE_SEPERATION:
                    close_boids.append(bo)
                else:
                    far_visible_boids.append(bo)

            boid.cohere(far_visible_boids)
            boid.align(far_visible_boids)
            boid.seperate(close_boids)
            
            #### END OF YOUR CODE ####

            # Keep within window bounds
            boid.keep_in_bounds()
            # Update the position based on the current velocity.
            boid.update_position()
            # Draw on screen
            pygame.draw.circle(screen, boid.color, (int(boid.position.x), int(boid.position.y)), 6)

        pygame.display.update()


main()
