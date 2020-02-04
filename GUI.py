import pygame


def main():
    screen = pygame.display.set_mode((800,800))
    pygame.display.set_caption("Maze")
    keep_running = True

    while keep_running:
        for event in pygame.event.get():
            if event.type == pygame.K_SPACE:
                keep_running = False


main()
pygame.quit()
