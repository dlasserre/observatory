from PIL import Image
import math

class CloudDetector:
    DYNAMIC_RATIO = 3
    x_max = y_max = []

    def in_radius(self, x, y) -> bool:
        if x < self.x_max and y < self.y_max:
            return True
        return False

    def create_radius(self, image, radius):
        x_matrix = y_matrix = []
        theta = 0.0
        x_max = max(range(image.size[0]))
        y_max = max(range(image.size[1]))
        x_center = int(len(range(image.size[0])) / 2)
        y_center = int(len(range(image.size[1])) / 2)
        while theta < 6.28: #pi x 2
            x = int(x_center + radius * math.cos(theta))
            y = int(y_center + radius * math.sin(theta))
            if x_max > x > 0 and 0 < y < y_max:
                x_matrix.append(x)
                y_matrix.append(y)
                image.putpixel((x, y), 222)
            theta = theta + 1.0/radius
        self.x_max = max(x_matrix)
        self.y_max = max(y_matrix)
        image.save('radius_'+str(radius)+'.png')

    @staticmethod
    def get_max(image, pixels_map) -> int : #need average for more accurate value...
        higher = 0
        for i in range(image.size[0]):  # for every pixel:
            for j in range(image.size[1]):
                if higher < pixels_map[i, j] < 255: #satured pixel
                    higher = pixels_map[i,j]
        return higher

    def percent_cloudy(self, image):
        pixels_map = image.load()
        higher = self.get_max(image, pixels_map)
        total_high = total = 0
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                if self.in_radius(x,y):
                    if pixels_map[x, y] >= higher / self.DYNAMIC_RATIO:
                        total_high = total_high + pixels_map[x, y]
                total = total + pixels_map[x,y]
        return round((total_high/total)*100)

img = Image.open('total-cloud.png', 'r')
# img = Image.open('clouds.png', 'r')
# img = Image.open('img-clear.png', 'r')
cloudy = CloudDetector()
cloudy.create_radius(img, 100)
print('---> '+str(cloudy.percent_cloudy(img))+"% cloud cover")
