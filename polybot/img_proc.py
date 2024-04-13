from pathlib import Path

import numpy as np
from matplotlib.image import (imread, imsave)
import cv2

def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self,angle):
        if not isinstance(angle, int):
            raise ValueError("Rotation angle must be an integer number of degrees.")
        image = np.array(self.data)
        rows, cols = image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)  # Rotation center and scale
        rotated_image = cv2.warpAffine(image, M, (cols, rows))
        self.data = rotated_image.tolist()

        # TODO remove the `raise` below, and write your implementation
        # raise NotImplementedError()

    def salt_n_pepper(self, noise_ratio=0.1):
        if not 0 <= noise_ratio <= 1:
            raise ValueError("Noise ratio must be between 0.0 and 1.0.")
        height, width = len(self.data), len(self.data[0])
        num_pixels = height * width
        num_noise_pixels = int(noise_ratio * num_pixels)
        noise_indices = np.random.choice(num_pixels, num_noise_pixels, replace=False)
        for idx in noise_indices:
            row = idx // width
            col = idx % width
        # TODO remove the `raise` below, and write your implementation
        # raise NotImplementedError()

    def concat(self, other_img, direction='horizontal'):
        if self.data[0][0] != other_img.data[0][0] or self.data[0][0] != 255:
            raise ValueError("Images must have compatible grayscale intensity range (0-255).")

            # Validate direction
        if direction not in ('horizontal', 'vertical'):
            raise ValueError("Direction must be 'horizontal' or 'vertical'.")

            # Concatenation logic
        if direction == 'horizontal':
            # Ensure both images have the same height
            if len(self.data) != len(other_img.data):
                # Pad the shorter image with zeros to match the height of the longer image
                height_diff = abs(len(self.data) - len(other_img.data))
                padding_row = [0] * len(self.data[0])
                if len(self.data) < len(other_img.data):
                    self.data.extend([padding_row] * height_diff)
                else:
                    other_img.data.extend([padding_row] * height_diff)

            # Concatenate image data by row
            self.data = [row1 + row2 for row1, row2 in zip(self.data, other_img.data)]

        else:  # direction == 'vertical'
            # Ensure both images have the same width
            if len(self.data[0]) != len(other_img.data[0]):
                # Pad the narrower image with zeros to match the width of the wider image
                width_diff = abs(len(self.data[0]) - len(other_img.data[0]))
                padding_value = [0] * width_diff
                if len(self.data[0]) < len(other_img.data[0]):
                    for row in self.data:
                        row.extend(padding_value)
                else:
                    for row in other_img.data:
                        row.extend(padding_value)

            # Concatenate image data by column
            self.data = [[pixel for row in (col1, col2) for pixel in row] for col1, col2 in
                         zip(*zip(self.data, other_img.data))]



        # TODO remove the `raise` below, and write your implementation
        # raise NotImplementedError()

    def segment(self):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()




    if my_img = Img()