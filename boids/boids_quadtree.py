import pygame
import random
from quadtree import QuadTree, Point, Rectangle
from statistics import mean


screen_size = 800
MARGIN = screen_size * 0.05


class Boid:
    NUM_BOIDS = 800
    DISTANCE_VISIBLE = 20
    DISTANCE_SEPERATION = 8
    MAX_SPEED = 2.0
    COHERENCE_FACTOR  = 0.01
    ALIGNMENT_FACTOR  = 0.05
    SEPARATION_FACTOR = 0.1
    
    def __init__(self, color=(0,255,255)):
        self.position = pygame.math.Vector2(random.randint(0, screen_size), random.randint(0, screen_size))
        self.velocity = pygame.math.Vector2(random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED), random.uniform(-Boid.MAX_SPEED, Boid.MAX_SPEED))
        self.velocity_buffer = self.velocity.copy()
        self.color = color
    
    def cohere(self, boids):
        if len(boids) > 0:
            c_o_mass = pygame.math.Vector2(mean([boid.position.x for boid in boids]),
                                           mean([boid.position.y for boid in boids]))

            self.velocity_buffer.x += (1 if (c_o_mass.x - self.position.x) > 0 else -1) * Boid.COHERENCE_FACTOR
            self.velocity_buffer.y += (1 if (c_o_mass.y - self.position.y) > 0 else -1) * Boid.COHERENCE_FACTOR
    
    def align(self, boids):
        if len(boids) > 0:
            c_o_vel = pygame.math.Vector2(mean([boid.velocity_buffer.x for boid in boids]),
                                          mean([boid.velocity_buffer.y for boid in boids]))

            self.velocity_buffer.x += (1 if (c_o_vel.y - self.velocity_buffer.y) > 0 else -1) * Boid.ALIGNMENT_FACTOR
            self.velocity_buffer.y += (1 if (c_o_vel.y - self.velocity_buffer.y) > 0 else -1) * Boid.ALIGNMENT_FACTOR
    
    def seperate(self, boids):
        if len(boids) > 0:
            c_o_mass = pygame.math.Vector2(mean([boid.position.x for boid in boids]),
                                           mean([boid.position.y for boid in boids]))

            self.velocity_buffer.x += (1 if (c_o_mass.x - self.position.x) < 0 else -1) * Boid.SEPARATION_FACTOR
            self.velocity_buffer.y += (1 if (c_o_mass.y - self.position.y) < 0 else -1) * Boid.SEPARATION_FACTOR
    
    def keep_in_bounds(self):
        TURN_FACTOR = 0.1
        turn = Boid.MAX_SPEED * TURN_FACTOR
        if self.position.x < MARGIN:
            self.velocity_buffer.x += turn
        if self.position.x > screen_size - MARGIN:
            self.velocity_buffer.x -= turn
        if self.position.y < MARGIN:
            self.velocity_buffer.y += turn
        if self.position.y > screen_size - MARGIN:
            self.velocity_buffer.y -= turn
    
    def update_position(self):
        if self.velocity_buffer.length() > Boid.MAX_SPEED:
            self.velocity_buffer *= 0.9
        self.velocity = self.velocity_buffer.copy()
        self.position += self.velocity


def closest_boids(boid, dist, boids):
    return [b for b in boids if b.position.distance_to(boid.position) <= dist and b != boid]


def main():
    global screen_size, screen_size
    pygame.init()
    screen = pygame.display.set_mode((screen_size, screen_size))
    
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
        
        # QuadTree root node
        qtree = QuadTree(Rectangle(screen_size/2, screen_size/2, screen_size/2, screen_size/2))
        # Inserting all boids (as points) into the quad tree
        for boid in boids:
            qtree.insert(Point(boid))

        for boid in boids:
            rect_range = Rectangle(boid.position.x, boid.position.y, Boid.DISTANCE_VISIBLE/2, Boid.DISTANCE_VISIBLE/2)
            # Retrieve only the boids located within quadrants that intersect with the specified rect_range

            inrange_boids = qtree.query(rect_range)

            
            #### YOUR CODE HERE (copy from boids.py) ####
            # use `inrange_boids` instead of `boids`

            visible_boids = [bo for bo in inrange_boids if bo != boid
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
            pygame.draw.circle(screen, boid.color, (int(boid.position.x), int(boid.position.y)), 2)
            
        # Draw QuadTree on screen
        qtree.draw(screen)
        
        # Draw rect_range around the zeroth boid
        #rect_range = Rectangle(boids[0].position.x, boids[0].position.y, Boid.DISTANCE_VISIBLE/2, Boid.DISTANCE_VISIBLE/2)
        #rect = pygame.Rect(rect_range.x - rect_range.hw, rect_range.y - rect_range.hh, rect_range.hw * 2, rect_range.hh * 2)
        #pygame.draw.rect(screen, (255,255,100), rect, 4)

        pygame.display.update()

main()
