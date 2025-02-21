import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen size and colors
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)  # Black background
BIG_CIRCLE_COLOR = (255, 255, 255)  # White for the large circle

# Circle and bubble settings
BIG_CIRCLE_RADIUS = SCREEN_WIDTH // 3  # Smaller big circle
BUBBLE_RADIUS = BIG_CIRCLE_RADIUS // 15  # Bigger bubbles relative to the smaller circle

# Define bubble speed
SPEED = 5  # Speed for bubble movement

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bubble Collision Simulation')

# Clock for controlling FPS
clock = pygame.time.Clock()

# Limit the maximum number of bubbles
MAX_BUBBLES = 100  # Set a limit on how many bubbles can exist

# Collision cooldown in frames (e.g., 10 frames)
COLLISION_COOLDOWN = 10

# Bubble class
class Bubble:
    def __init__(self, x, y, dx, dy, color, can_generate=True):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.can_generate = can_generate  # Indicates if the bubble can generate new bubbles on collision

    def move(self):
        # Move the bubble
        self.x += self.dx
        self.y += self.dy

        # Check for collisions with the circle wall
        if self.distance_from_center() + BUBBLE_RADIUS > BIG_CIRCLE_RADIUS:
            self.adjust_position_and_reflect()

    def distance_from_center(self):
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        return math.sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)

    def adjust_position_and_reflect(self):
        # Get the normal vector (from the center to the current position)
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        normal_x = self.x - center_x
        normal_y = self.y - center_y

        # Normalize the normal vector
        normal_length = math.sqrt(normal_x ** 2 + normal_y ** 2)
        normal_x /= normal_length
        normal_y /= normal_length

        # Calculate the dot product of velocity and the normal
        dot_product = self.dx * normal_x + self.dy * normal_y

        # Reflect the velocity vector using the reflection formula
        self.dx = self.dx - 2 * dot_product * normal_x
        self.dy = self.dy - 2 * dot_product * normal_y

        # Adjust the position to ensure the bubble stays inside the boundary
        excess_distance = (self.distance_from_center() + BUBBLE_RADIUS) - BIG_CIRCLE_RADIUS
        self.x -= normal_x * excess_distance
        self.y -= normal_y * excess_distance

    def check_collision(self, other):
        # Check if two bubbles are colliding
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < 2 * BUBBLE_RADIUS

    def draw(self, surface):
        # Draw the bubble with its own color
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BUBBLE_RADIUS)

# Function to create random color bubbles
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Initialize bubbles with random colors
bubbles = [
    Bubble(
        SCREEN_WIDTH // 2 + random.randint(-BIG_CIRCLE_RADIUS + BUBBLE_RADIUS, BIG_CIRCLE_RADIUS - BUBBLE_RADIUS),
        SCREEN_HEIGHT // 2 + random.randint(-BIG_CIRCLE_RADIUS + BUBBLE_RADIUS, BIG_CIRCLE_RADIUS - BUBBLE_RADIUS),
        random.choice([-SPEED, SPEED]),
        random.choice([-SPEED, SPEED]),
        random_color(),
        can_generate=True  # The first two bubbles can generate new bubbles
    ) for _ in range(2)
]

# Store pairs of bubbles that have already collided, and their cooldown time
collision_cooldowns = {}

def draw_big_circle():
    # Draw the big circle in the center
    pygame.draw.circle(screen, BIG_CIRCLE_COLOR, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), BIG_CIRCLE_RADIUS, 2)

def main():
    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_big_circle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move and draw bubbles
        current_collisions = []  # To track current collisions

        for i, bubble in enumerate(bubbles):
            bubble.move()
            bubble.draw(screen)

            # Check for collisions between bubbles
            for j, other_bubble in enumerate(bubbles):
                if i < j and bubble.check_collision(other_bubble):
                    # Create a unique collision pair key
                    collision_pair = tuple(sorted((i, j)))

                    # Check if this collision is in the cooldown state
                    if collision_pair not in collision_cooldowns and len(bubbles) < MAX_BUBBLES:
                        # Add a new bubble at the midpoint of the two colliding bubbles
                        if bubble.can_generate and other_bubble.can_generate:
                            new_bubble = Bubble(
                                (bubble.x + other_bubble.x) / 2,
                                (bubble.y + other_bubble.y) / 2,
                                random.choice([-SPEED, SPEED]),
                                random.choice([-SPEED, SPEED]),
                                random_color(),
                                can_generate=False  # New bubbles cannot generate more bubbles
                            )
                            bubbles.append(new_bubble)

                        # Start the cooldown timer for this pair
                        collision_cooldowns[collision_pair] = COLLISION_COOLDOWN

                    # Add the current collision to the list
                    current_collisions.append(collision_pair)

        # Update the cooldowns
        for pair in list(collision_cooldowns.keys()):
            collision_cooldowns[pair] -= 1
            if collision_cooldowns[pair] <= 0:
                del collision_cooldowns[pair]

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()