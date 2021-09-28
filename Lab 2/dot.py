from PIL import Image, ImageDraw, ImageFont
import random

# image = Image.new("RGB", (135, 240))
# draw = ImageDraw.Draw(image)

class Dot:
    def __init__(self, draw, display_dim, dot_size, org_coord):
        self.dim = display_dim
        self.size = dot_size
        self.rand_coord = self.get_random_ellipse_coord()
        self.org_coord = org_coord
        self.pos = self.rand_coord.copy()
        self.color = self.get_color()
        self.draw = draw
        

    def get_random_ellipse_coord(self):
        x0 = random.randint(0, self.dim[0] - self.size)
        y0 = random.randint(0, self.dim[1] - self.size)
        x1 = x0 + self.size
        y1 = y0 + self.size
        return [x0, y0, x1, y1]

    def get_color(self):
        r = random.randint(30, 255)
        g = random.randint(30, 255)
        b = random.randint(30, 255)
        return (r, g, b)

    def go_org(self):
        # Move dots to organized coordinations
        if self.pos[0] < self.org_coord[0]:
            self.pos[0] += 1
        elif self.pos[0] > self.org_coord[0]:
            self.pos[0] -= 1

        if self.pos[1] < self.org_coord[1]:
            self.pos[1] += 1
        elif self.pos[1] > self.org_coord[1]:
            self.pos[1] -= 1
            
        self.pos[2] = self.pos[0] + self.size
        self.pos[3] = self.pos[1] + self.size

    def go_rand(self):
        # Move dots to original random coordinations
        if self.pos[0] < self.rand_coord[0]:
            self.pos[0] += 1
        elif self.pos[0] > self.rand_coord[0]:
            self.pos[0] -= 1

        if self.pos[1] < self.rand_coord[1]:
            self.pos[1] += 1
        elif self.pos[1] > self.rand_coord[1]:
            self.pos[1] -= 1

        

        self.pos[2] = self.pos[0] + self.size
        self.pos[3] = self.pos[1] + self.size


    def show(self):
        self.draw.ellipse(self.pos, fill=self.color, outline=None)