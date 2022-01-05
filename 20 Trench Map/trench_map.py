# https://adventofcode.com/2021/day/20

input_file = 'real_input.txt'
#input_file = 'test_input.txt'

with open(input_file) as file:
    lines = [line.strip() for line in file.readlines()]


class InfiniteImage:
    def __init__(self, image):
        self.x_min = 0
        self.x_max = len(image[0]) - 1
        self.y_min = 0
        self.y_max = len(image) - 1
        self.infinty_value = 0
        """Current image
        0 1
        1 0
        """
        self.pixels = {}
        for y in range(0, self.y_max+1):
            for x in range(0, self.x_max+1):
                if image[y][x] == '#':
                    self.pixels[(x, y)] = 1
                else:
                    self.pixels[(x, y)] = 0
        self.padding_1 = self.generate_padding(1)
        self.padding_2 = self.generate_padding(2)

    def generate_padding(self, layer):
        # Generate padding around image to account for infinte grid
        if layer == 1:
            """
            0 0 0 0
            0 i i 0
            0 i i 0
            0 0 0 0
            """
            x_min = self.x_min
            x_max = self.x_max
            y_min = self.y_min
            y_max = self.y_max
        elif layer == 2:
            """
            0 0 0 0 0 0
            0         0
            0   i i   0
            0   i i   0
            0         0
            0 0 0 0 0 0
            """
            x_min = self.x_min - 1
            x_max = self.x_max + 1
            y_min = self.y_min - 1
            y_max = self.y_max + 1
        padding = {}
        for x in range(x_min-1, x_max+2):
            padding[(x, y_min-1)] = self.infinty_value
            padding[(x, y_max+1)] = self.infinty_value
        for y in range(y_min, y_max+1):
            padding[(x_min-1, y)] = self.infinty_value
            padding[(x_max+1, y)] = self.infinty_value
        return padding

    def get_enhance_index(self, pixel):
        x = pixel[0]
        y = pixel[1]
        l = (x-1, y)
        r = (x+1, y)
        up = (x, y-1)
        up_l = (x-1, y-1)
        up_r = (x+1, y-1)
        down = (x, y+1)
        down_l = (x-1, y+1)
        down_r = (x+1, y+1)
        """Positions -> 9 bits: 876543210
        8 7 6
        5(4)3
        2 1 0
        """
        pos = 8
        index = 0
        for coord in (up_l, up, up_r, l, pixel, r, down_l, down, down_r):
            neighbor = self.pixels.get(coord)
            if neighbor is None:
                neighbor = self.padding_1.get(coord)
            if neighbor is None:
                neighbor = self.infinty_value
            if neighbor == 1:
                index = index | (1 << pos)
            pos -= 1
        return index

    def apply_algorithm(self, pixels):
        enhanced_pixels = {}
        for pixel in pixels:
            index = self.get_enhance_index(pixel)
            new_val = (algorithm & (1 << index)) >> index
            enhanced_pixels[pixel] = new_val
        return enhanced_pixels

    def enhance(self, times):
        for i in range(times):
            # Add inner padding to image
            self.pixels.update(self.padding_1)
            # Update image size
            self.x_min -= 1
            self.x_max += 1
            self.y_min -= 1
            self.y_max += 1
            # Generate new padding
            self.padding_1 = self.padding_2
            self.padding_2 = self.generate_padding(2)

            # Enhance
            enhanced_pixels = self.apply_algorithm(self.pixels)
            enhanced_padding_1 = self.apply_algorithm(self.padding_1)
            enhanced_padding_2 = self.apply_algorithm(self.padding_2)

            # Update pixels and padding
            self.pixels = enhanced_pixels
            self.padding_1 = enhanced_padding_1
            self.padding_2 = enhanced_padding_2

            # Determine new infinity value
            if self.infinty_value == 0:
                """
                0 0 0
                0(0)0
                0 0 0
                """
                self.infinty_value = (algorithm & 1)
            elif self.infinty_value == 1:
                """
                1 1 1
                1(1)1
                1 1 1
                """
                self.infinty_value = (algorithm & (
                    1 << int('111111111', 2))) >> int('111111111', 2)

    def count_lit(self):
        # Count lit pixels
        lit_count = 0
        for val in self.pixels.values():
            if val == 1:
                lit_count += 1
        return lit_count


# Set up algorithm
alg = list(lines[0])
algorithm = 0
for i, char in enumerate(alg):
    if char == '#':
        algorithm = algorithm | (1 << i)

# Set up image
img = [list(i) for i in lines[2:]]

# Part 1
image = InfiniteImage(img)
image.enhance(2)
print(f"Part 1: {image.count_lit()}")

# Part 2
image = InfiniteImage(img)
image.enhance(50)
print(f"Part 2: {image.count_lit()}")
