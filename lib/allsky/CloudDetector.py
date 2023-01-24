from PIL import Image, ImageDraw, ImageFont
import math


class CloudDetector:
    x_center = y_center = 0
    radius = 0
    # Weighted average values. (modify if u want)
    grey_scale = [(0, 0), (1, 0.5), (2, 6), (3, 9), (4, 9.5), (5, 10), (6, 10.5), (7, 11)]

    def in_radius(self, x, y) -> bool:
        distance = self.dist_from_radius_center((x, y))
        if distance < self.radius:
            return True
        return False

    def dist_from_radius_center(self, pixel):
        xd = abs(pixel[0] - self.x_center)
        yd = abs(pixel[1] - self.y_center)
        return math.sqrt((xd*xd)+(yd*yd))

    def _init_radius(self, image, radius):
        theta = 0.0
        self.radius = radius
        x_max = max(range(image.size[0]))
        y_max = max(range(image.size[1]))
        self.x_center = int(len(range(image.size[0])) / 2)
        self.y_center = int(len(range(image.size[1])) / 2)
        while theta < 6.28: #pi x 2
            x = int(self.x_center + radius * math.cos(theta))
            y = int(self.y_center + radius * math.sin(theta))
            if x_max > x > 0 and 0 < y < y_max:
                image.putpixel((x, y), 222)
            theta = theta + 1.0/radius

    def get_greyscale_average(self, image, pixels_map):
        width, height = image.size
        total = number = 0
        for x in range(0, width):
            for y in range(0, height):
                if self.in_radius(x, y):
                    total += pixels_map[x, y]
                    number += 1
        return total / number

    @staticmethod
    def debug(image, percent):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 100)
        draw.text((50, 50), percent+'% clouds', fill=255, font=font)
        image.save('result_'+image.filename)

    @staticmethod
    def split_histogram(histogram):
        matrix = []
        for split_histo in histogram:
            matrix.append(sum(split_histo))
        return matrix

    def percent_cloudy(self, path_to_img, radius, debug=True):
        image = Image.open(path_to_img, 'r')
        average = divisor = 0
        split = 32
        self._init_radius(image, radius)
        mask = Image.new("L", image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((
            self.x_center - self.radius,
            self.y_center - self.radius,
            self.x_center + self.radius,
            self.y_center + self.radius), fill=255)
        histogram = image.histogram(mask)
        result = [histogram[idx:idx+split] for idx in range(0, len(histogram), split)]
        matrix = self.split_histogram(result)
        for coefficient in self.grey_scale:
            average += matrix[coefficient[0]] * coefficient[1]
            divisor += matrix[coefficient[0]]
        percent = round((average/divisor) * 100 / 8)
        percent = percent if percent < 100 else 100
        if debug:
            self.debug(image, str(percent))
        return percent
