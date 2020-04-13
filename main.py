
import pygame
import sys
import numpy as np

import random
random.seed(43)



try:

    nb_maps = 20
    radius = 24
    sizeX = 640

    pygame.init()
    fpsClock = pygame.time.Clock()
    window = pygame.display.set_mode((sizeX, sizeX), 1)



    from hexmap.map import Map
    from hexmap.render import RenderGrid
    maps = [Map(3, 3) for i in range(nb_maps)]

    offset = 3.1 * radius * np.sqrt(3)
    nb_per_row = 5

    grids = [RenderGrid(m, offset_x=offset * (idx % nb_per_row),
                        offset_y=offset * (idx // nb_per_row), sizeX=sizeX, radius=radius)
             for idx, m in enumerate(maps)]




    from pygame.locals import QUIT, MOUSEBUTTONDOWN

    # Leave it running until exit
    idx = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        window.fill(pygame.Color('white'))
        for grid in grids:
            grid.draw()
            window.blit(grid, (0, 0))
        for grid in grids:
            grid.draw_lines()
            window.blit(grid, (0, 0))
        pygame.display.update()
        fpsClock.tick(10)
        if idx == 4:
            pygame.image.save(window, "result.png")
        idx += 1
finally:
    pygame.quit()