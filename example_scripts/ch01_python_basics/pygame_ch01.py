import pygame

# Initialize Pygame
pygame.init()

# Open a Pygame window
win = pygame.display.set_mode((400,300))

# Draw a circle
win.fill((0,0,0))
pygame.draw.circle(win, (255,0,0), (200,150), 30)
pygame.display.flip()

# Show the window for 30 seconds
pygame.time.wait(30000)

# Quit Pygame
pygame.quit()
