import pygame
import random
import math
from itertools import combinations

# Initialize Pygame
pygame.init()

# Screen size and colors
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)  # Black background
BIG_CIRCLE_COLOR = (255, 255, 255)  # White for the large circle

# Circle and bubble settings
BIG_CIRCLE_RADIUS = SCREEN_WIDTH // 3  # Smaller big circle
BUBBLE_RADIUS = BIG_CIRCLE_RADIUS // 15  # Relative bubble size

# Define bubble speed
SPEED = 5  # Increase speed for faster movement

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bubble Collision Simulation')

# Clock for controlling FPS
clock = pygame.time.Clock()

# Limit the maximum number of bubbles
MAX_BUBBLES = 100  # Set a limit on how many bubbles can exist

# Bubble class
class Bubble:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color

    def move(self):
        # Move the bubble
        self.x += self.dx
        self.y += self.dy

        # Check for collisions with the circle wall
        if self.distance_from_center() + BUBBLE_RADIUS > BIG_CIRCLE_RADIUS:
            self.reflect()

        # Ensure the bubble stays within the boundary after reflection
        self.ensure_within_boundary()

    def distance_from_center(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        return math.sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)

    def reflect(self):
        # Get the normal vector (from the center to the current position)
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        normal_x = self.x - center_x
        normal_y = self.y - center_y

        # Normalize the normal vector
        normal_length = math.sqrt(normal_x ** 2 + normal_y ** 2)
        if normal_length == 0:
            return  # Prevent division by zero
        normal_x /= normal_length
        normal_y /= normal_length

        # Calculate the dot product of velocity and the normal
        dot_product = self.dx * normal_x + self.dy * normal_y

        # Reflect the velocity vector using the reflection formula
        self.dx = self.dx - 2 * dot_product * normal_x
        self.dy = self.dy - 2 * dot_product * normal_y

    def ensure_within_boundary(self):
        # Adjust position to ensure the bubble is within the boundary
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        distance = self.distance_from_center()
        if distance + BUBBLE_RADIUS > BIG_CIRCLE_RADIUS:
            overlap = distance + BUBBLE_RADIUS - BIG_CIRCLE_RADIUS
            if distance != 0:
                self.x -= (overlap * (self.x - center_x)) / distance
                self.y -= (overlap * (self.y - center_y)) / distance
            else:
                # If at the center, move randomly within boundary
                angle = random.uniform(0, 2 * math.pi)
                self.x = center_x + (BIG_CIRCLE_RADIUS - BUBBLE_RADIUS) * math.cos(angle)
                self.y = center_y + (BIG_CIRCLE_RADIUS - BUBBLE_RADIUS) * math.sin(angle)

    def check_collision(self, other):
        # Check if two bubbles are colliding
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < 2 * BUBBLE_RADIUS

    def draw(self, surface):
        # Draw the bubble with its own color
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BUBBLE_RADIUS)

# Function to create random color bubbles
def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))

# Initialize bubbles with random colors
def initialize_bubbles(num_bubbles):
    bubbles = []
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    for _ in range(num_bubbles):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, BIG_CIRCLE_RADIUS - BUBBLE_RADIUS)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        dx = random.choice([-SPEED, SPEED]) * math.cos(random.uniform(0, 2 * math.pi))
        dy = random.choice([-SPEED, SPEED]) * math.sin(random.uniform(0, 2 * math.pi))
        color = random_color()
        bubbles.append(Bubble(x, y, dx, dy, color))
    return bubbles

bubbles = initialize_bubbles(2)  # Start with 2 bubbles

def draw_big_circle():
    # Draw the big circle in the center
    pygame.draw.circle(screen, BIG_CIRCLE_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), BIG_CIRCLE_RADIUS, 2)

def main():
    running = True
    collided_pairs = set()  # To keep track of collided pairs

    while running:
        screen.fill(BG_COLOR)
        draw_big_circle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move and draw bubbles
        for bubble in bubbles:
            bubble.move()
            bubble.draw(screen)

        # Check for collisions between unique pairs
        new_bubbles = []
        for bubble1, bubble2 in combinations(bubbles, 2):
            if bubble1.check_collision(bubble2):
                pair = tuple(sorted((id(bubble1), id(bubble2))))
                if pair not in collided_pairs:
                    if len(bubbles) + len(new_bubbles) < MAX_BUBBLES:
                        # Add one new bubble on collision with random colors
                        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                        new_x = (bubble1.x + bubble2.x) / 2
                        new_y = (bubble1.y + bubble2.y) / 2
                        angle = random.uniform(0, 2 * math.pi)
                        new_dx = SPEED * math.cos(angle)
                        new_dy = SPEED * math.sin(angle)
                        new_color = random_color()
                        new_bubbles.append(Bubble(new_x, new_y, new_dx, new_dy, new_color))
                        # Mark this pair as collided
                        collided_pairs.add(pair)

        # Reset collided pairs at the end of each frame
        collided_pairs.clear()

        # Add the new bubbles after checking for collisions (but ensure we don't exceed max bubbles)
        bubbles.extend(new_bubbles)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
        main()