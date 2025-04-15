import pygame
import math

# Initialize Pygame
pygame.init()

# constants
Width_monitor = 1920
Height_monitor = 1080
Character_spacing_x_direction = 10
Character_spacing_y_direction = 20
Rotation_speed_angle_A = 0.07
Rotation_speed_angle_B = 0.03

ASCII_Character = ".,-~:;=o*?#%$@"

# parameters for the torus
R1 = 1  # thickness of the Torus
R2 = 2  # Radius of Torus
K2 = 5  # Distance from viewer to object
K3 = 8

# Create the main display window
screen = pygame.display.set_mode((Width_monitor, Height_monitor))
pygame.display.set_caption('Rotating Donut')

font = pygame.font.SysFont('Arial', 18, bold=True)

# Determine how many character cells fit on the screen
Num_rows = Height_monitor // Character_spacing_y_direction
Num_columns = Width_monitor // Character_spacing_x_direction
Screen_Character_count = Num_rows * Num_columns

# Render the character as white text at position (x, y)
def rendering_characters(char, x, y):
    text = font.render(char, True, (255, 255, 255))
    screen.blit(text, (x, y))  # Draw to screen


def main():
    A = B = 0
    running = True

    while running:
        screen.fill((0, 0, 0))  # Black screen

        # Initialize buffers to store depth values (for each character) and character output (to be rendered)
        depth_buffer = [0] * Screen_Character_count
        output = [' '] * Screen_Character_count

        # Calculate the 3D donut points projected to 2D
        for theta in range(0, 628, 15):  # 0 to 2π
            for phi in range(0, 628, 2):
                sin_phi = math.sin(phi * 0.01)  # scale down to radians
                cos_phi = math.cos(phi * 0.01)

                sin_theta = math.sin(theta * 0.01)
                cos_theta = math.cos(theta * 0.01)

                sin_A = math.sin(A)
                cos_A = math.cos(A)
                sin_B = math.sin(B)
                cos_B = math.cos(B)

                Factor1 = cos_theta * R1 + R2
                Factor2 = sin_theta * R1
                Factor3 = Factor2 * cos_A - sin_phi * sin_A * Factor1

                z_depth = 1 / (sin_phi * Factor1 * cos_A + Factor2 * sin_A + K2)

                # Calculate 2D screen coordinates
                x = int(Num_columns / 2 + z_depth * 40 * (cos_phi * cos_B * Factor1 - sin_B * Factor3))
                y = int(Num_rows / 2 + z_depth * 20 * (cos_phi * sin_B * Factor1 + cos_B * Factor3))  # 20 is a Factor

                # Calculate luminance N based on surface normal and lighting direction
                N = int(K3 * ((sin_theta * cos_A - sin_phi * cos_theta * sin_A) * cos_B - sin_phi * cos_theta * cos_A - sin_theta * sin_A + cos_phi * cos_theta * sin_B))

                pixel_index = int(x + Num_columns * y) # convert 2D to 1D index

                # Check if the point is within screen bounds and closer than previous points
                if (0 <= y < Num_rows) and (0 <= x < Num_columns) and (z_depth > depth_buffer[pixel_index]):
                    depth_buffer[pixel_index] = z_depth

                    # Convert light intensity to corresponding ASCII character
                    char_index = max(0, min(N,len(ASCII_Character) - 1))
                    output[pixel_index] = ASCII_Character[char_index]


        # Render all characters for the current frame
        for i in range(Screen_Character_count):
            char = output[i]
            if char != ' ':
                # Calculate the x and y pixel for characters (Convert 1D index back to 2D)
                x = (i % Num_columns) * Character_spacing_x_direction
                y = (i // Num_columns) * Character_spacing_y_direction
                rendering_characters(char, x, y)

        # Update rotation
        A += Rotation_speed_angle_A
        B += Rotation_speed_angle_B

        # Update display
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                running = False


if __name__ == "__main__":
    main()
    pygame.quit()