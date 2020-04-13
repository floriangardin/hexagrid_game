from abc import ABCMeta, abstractmethod
import pygame
import pygame.gfxdraw
import math
from hexmap.map import Grid
from .map import Map, MapUnit

SQRT3 = math.sqrt(3)




class Render(pygame.Surface):
    __metaclass__ = ABCMeta

    def __init__(self, map, offset_x=0, offset_y=0, radius=24, sizeX=640, *args, **keywords):
        self.map = map
        self.radius = radius
        self.offset_x = offset_x
        self.offset_y = offset_y
        # Colors for the map
        self.GRID_COLOR = pygame.Color(0, 0, 0)
        self.sizeX = sizeX

        super(Render, self).__init__((self.width, self.height), pygame.SRCALPHA, *args, **keywords)

        self.cell = [(.5 * self.radius, 0),
                     (1.5 * self.radius, 0),
                     (2 * self.radius, SQRT3 / 2 * self.radius),
                     (1.5 * self.radius, SQRT3 * self.radius),
                     (.5 * self.radius, SQRT3 * self.radius),
                     (0, SQRT3 / 2 * self.radius)
                     ]

    def get_surface(self, row, col):
        """
        Returns a subsurface corresponding to the surface, hopefully with trim_cell wrapped around the blit method.
        """
        width = 2 * self.radius
        height = self.radius * SQRT3

        top = (row - math.ceil(col / 2.0)) * height + (height / 2 if col % 2 == 1 else 0)
        left = 1.5 * self.radius * col
        print(top, left)
        return self.subsurface(pygame.Rect(left, top, width, height))

    @property
    def width(self):
        return self.sizeX

    @property
    def height(self):
        return self.sizeX



    # Identify cell
    def get_cell(self, x, y):
        """
		Identify the cell clicked in terms of row and column
		"""
        # Identify the square grid the click is in.
        row = math.floor(y / (SQRT3 * self.radius))
        col = math.floor(x / (1.5 * self.radius))

        # Determine if cell outside cell centered in this grid.
        x = x - col * 1.5 * self.radius
        y = y - row * SQRT3 * self.radius

        # Transform row to match our hex coordinates, approximately
        row = row + math.floor((col + 1) / 2.0)

        # Correct row and col for boundaries of a hex grid
        if col % 2 == 0:
            if y < SQRT3 * self.radius / 2 and x < .5 * self.radius and \
                            y < SQRT3 * self.radius / 2 - x:
                row, col = row - 1, col - 1
            elif y > SQRT3 * self.radius / 2 and x < .5 * self.radius and \
                            y > SQRT3 * self.radius / 2 + x:
                row, col = row, col - 1
        else:
            if x < .5 * self.radius and abs(y - SQRT3 * self.radius / 2) < SQRT3 * self.radius / 2 - x:
                row, col = row - 1, col - 1
            elif y < SQRT3 * self.radius / 2:
                row, col = row - 1, col

        return (row, col) if self.map.valid_cell((row, col)) else None

    def fit_window(self, window):
        top = max(window.get_height() - self.height, 0)
        left = max(window.get_width() - map.width, 0)
        return (top, left)




def draw_line(surf, points, color, thickness=1):

    for idx in range(thickness):
        points_ = [(i+idx, j+idx) for i, j in points]
        pygame.draw.polygon(surf, color, points_, thickness)
        #pygame.draw.aalines(surf, color, True, points)

class RenderGrid(Render):
    def draw(self):
        """
		Draws a hex grid, based on the map object, onto this Surface
		"""
        # A point list describing a single cell, based on the radius of each hex
        for col in range(self.map.cols):
            # Alternate the offset of the cells based on column
            offset = self.radius * SQRT3 / 2 if col % 2 else 0
            for row in range(self.map.rows):
                if (col == 0 or col == 2) and (row == 0):
                    continue
                # Calculate the offset of the cell
                top = offset + SQRT3 * row * self.radius + self.offset_y
                left = 1.5 * col * self.radius + self.offset_x
                # Create a point list containing the offset cell
                points = [(x + left, y + top) for (x, y) in self.cell]
                # Draw the polygon onto the surface
                white_color = (255, 255, 255, 255)
                color = self.map.colors[row][col]
                if color is not None:
                    pygame.gfxdraw.filled_polygon(self, points, color)
                    #self.blit(color.copy(), (left, top), None, pygame.BLEND_RGBA_MULT)
                    #del sub
                    #self.blit(sub, (left, top))

    def draw_lines(self):
        # A point list describing a single cell, based on the radius of each hex
        for col in range(self.map.cols):
            # Alternate the offset of the cells based on column
            offset = self.radius * SQRT3 / 2 if col % 2 else 0
            for row in range(self.map.rows):
                if (col == 0 or col == 2) and (row == 0):
                    continue
                # Calculate the offset of the cell
                top = offset + SQRT3 * row * self.radius + self.offset_y
                left = 1.5 * col * self.radius + self.offset_x
                # Create a point list containing the offset cell
                points = [(x + left, y + top) for (x, y) in self.cell]
                # Draw the polygon onto the surface
                draw_line(self, points, self.GRID_COLOR, thickness=2)

