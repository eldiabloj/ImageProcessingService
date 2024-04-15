# from pathlib import Path
#
# import cv2
# import numpy as np
# from matplotlib.images import (imread, imsave)
#
#
# def rgb2gray(rgb):
#     r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
#     gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
#     return gray
#
#
# class Img:
#
#     def __init__(self, path):
#         """
#         Do not change the constructor implementation
#         """
#         self.path = Path(path)
#         self.data = rgb2gray(imread(path)).tolist()
#
#     def save_img(self):
#         """
#         Do not change the below implementation
#         """
#         new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
#         imsave(new_path, self.data, cmap='gray')
#         return new_path
#
#     def blur(self, blur_level=16):
#
#         height = len(self.data)
#         width = len(self.data[0])
#         filter_sum = blur_level ** 2
#
#         result = []
#         for i in range(height - blur_level + 1):
#             row_result = []
#             for j in range(width - blur_level + 1):
#                 sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
#                 average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
#                 row_result.append(average)
#             result.append(row_result)
#
#         self.data = result
#
#     def contour(self):
#         for i, row in enumerate(self.data):
#             res = []
#             for j in range(1, len(row)):
#                 res.append(abs(row[j-1] - row[j]))
#
#             self.data[i] = res
#
#     def rotate(self, angle):
#         if not isinstance(angle, int):
#             raise ValueError("Rotation angle must be an integer number of degrees.")
#         images = np.array(self.data)
#         rows, cols = images.shape
#         m = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)  # Rotation center and scale
#         rotated_image = cv2.warpAffine(images, m, (cols, rows))
#         self.data = rotated_image.tolist()
#
#     def salt_n_pepper(self, noise_ratio=0.1):
#         if not 0 <= noise_ratio <= 1:
#             raise ValueError("Noise ratio must be between 0.0 and 1.0.")
#         height, width = len(self.data), len(self.data[0])
#         num_pixels = height * width
#         num_noise_pixels = int(noise_ratio * num_pixels)
#         noise_indices = np.random.choice(num_pixels, num_noise_pixels, replace=False)
#         for idx in noise_indices:
#             row = idx // width
#             col = idx % width
#
#     def concat(self, other_img, direction='horizontal'):
#         if self.data[0][0] != other_img.data[0][0] or self.data[0][0] != 255:
#             raise ValueError("Images must have compatible grayscale intensity range (0-255).")
#
#         if direction not in ('horizontal', 'vertical'):
#             raise ValueError("Direction must be 'horizontal' or 'vertical'.")
#
#         if direction == 'horizontal':
#             if len(self.data) != len(other_img.data):
#                 height_diff = abs(len(self.data) - len(other_img.data))
#                 padding_row = [0] * len(self.data[0])
#                 if len(self.data) < len(other_img.data):
#                     self.data.extend([padding_row] * height_diff)
#                 else:
#                     other_img.data.extend([padding_row] * height_diff)
#
#             self.data = [row1 + row2 for row1, row2 in zip(self.data, other_img.data)]
#
#         else:  # direction == 'vertical'
#             if len(self.data[0]) != len(other_img.data[0]):
#                 width_diff = abs(len(self.data[0]) - len(other_img.data[0]))
#                 padding_value = [0] * width_diff
#                 if len(self.data[0]) < len(other_img.data[0]):
#                     for row in self.data:
#                         row.extend(padding_value)
#                 else:
#                     for row in other_img.data:
#                         row.extend(padding_value)
#
#             self.data = [[pixel for row in (col1, col2) for pixel in row] for col1, col2 in
#                          zip(*zip(self.data, other_img.data))]
#
#     def segment(self, threshold=128):
#         if not 0 <= threshold <= 255:
#             raise ValueError("Threshold value must be between 0 and 255 (grayscale intensity).")
#
#         segmented_data = [[pixel if pixel > threshold else 0 for pixel in row] for row in self.data]
#
#         self.data = segmented_data
#
# my_img = Img('polybot/img/ojimg.jpg')
# self.path= img
# img.blur(blur_level=32)
# new_path = img.save_img()
# img.rotate(angle=45)
# img.concat(other_img, direction='horizontal')
# img.segment(threshold=100)
#
# u_in = input()
#
#
# if u_in == 'save':
#     save_img = Img.save_img('.img/ojimg.jpg')
#
# elif u_in == 'blur':
#     blur_img = Img('.img/ojimg.jpg')
#     blur_img = blur_img.blur()
#     cv2.imshow('Blurred Image', blur_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
#
# elif u_in == 'contour':
#     contour_img = Img.contour('.img/ojimg.jpg')
#     contour_img.show()
#
# elif u_in == 'rotate':
#     rotated_image = Img('.img/ojimg.jpg')
#     rotated_image = rotated_image.rotate(90)
#     rotated_image.show()
#
# elif u_in == 'salt_n_pepper':
#     salt_n_pepper_img = Img.salt_n_pepper('.img/ojimg.jpg')
#     salt_n_pepper_img.show()
#
# elif u_in == 'concat':
#     concat_img = Img.concat('.img/ojimg.jpg')
#     concat_img.show()
#
# elif u_in == 'segment':
#     num_clusters = 100
#     segment_img = Img('.img/ojimg.jpg')
#     segment_img = segment_img.segment(num_clusters)
#     cv2.imshow('Segmented Image', segment_img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

from pathlib import Path
import os
from PIL import Image
import cv2
import numpy as np

class Img:
    def __init__(self,image_path):
        self.image_path = image_path
        self.image_data = self.load_image()

    def load_image(self):
        try:
            image = cv2.imread(self.image_path)
            if image is not None:
                return image
            else:
                raise FileNotFoundError("Unable to load image.")
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def save_image(self, image_data, suffix='_filtered'):
        try:
            directory = 'images'
            if not os.path.exists(directory):
                os.makedirs(directory)

            path_obj = Path(self.image_path)
            file_path = os.path.join(directory, "{}{}{}".format(path_obj.stem, suffix, path_obj.suffix))
            cv2.imwrite(file_path, image_data)
            print(f"Image saved successfully: {file_path}")
        except Exception as e:
            print(f"Error saving image: {e}")

    def blur(self, blur_level=16):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            blur_level = max(1, blur_level)
            blur_level = blur_level + 1 if blur_level % 2 == 0 else blur_level
            blurred_image = cv2.GaussianBlur(self.image_data, (blur_level, blur_level), 0)
            self.save_image(blurred_image, '_blur')
            return blurred_image
        except Exception as e:
            print(f"Error applying blur: {e}")
            return None


    def rotate(self):
        try:
            img = cv2.imread(self.image_path)
            if img is None:
                raise FileNotFoundError("Unable to load image.")
            rotated_img = cv2.rotate(img, cv2.ROTATE_180)
            self.save_image(rotated_img, '_rotated')
            return rotated_img
        except Exception as e:
            print(f"Error rotating image: {e}")
            return None

    def salt_n_pepper(self, amount=0.05):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            noisy_image = self.image_data.copy()
            mask = np.random.choice([0, 1, 2], size=noisy_image.shape[:2], p=[amount / 2, amount / 2, 1 - amount])
            noisy_image[mask == 0] = 0
            noisy_image[mask == 1] = 255
            self.save_image(noisy_image, '_salt_n_pepper')
            return noisy_image
        except Exception as e:
            print(f"Error adding salt and pepper noise: {e}")
            return None

    def concat(self, other_image_data, direction='horizontal'):
        try:
            if self.image_data is None or other_image_data is None:
                raise ValueError("Image data is missing.")
            if direction not in ['horizontal', 'vertical']:
                raise ValueError("Invalid direction. Please use 'horizontal' or 'vertical'.")

            if direction == 'horizontal':
                concatenated_img = np.concatenate((self.image_data, other_image_data), axis=1)
            else:
                concatenated_img = np.concatenate((self.image_data, other_image_data), axis=0)
            self.save_image(concatenated_img, '_concat')
            return concatenated_img
        except Exception as e:
            print(f"Error concatenating images: {e}")
            return None

    def segment(self, num_clusters=100):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            image_rgb = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            pixels = image_rgb.reshape((-1, 3))
            pixels = np.float32(pixels)
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            centers = np.uint8(centers)
            segmented_image = centers[labels.flatten()]
            segmented_image = segmented_image.reshape(image_rgb.shape)

            # Darken the segmented image
            segmented_image = segmented_image * 0.5  # Reduce brightness by 50%

            self.save_image(segmented_image, '_segment')
            return segmented_image
        except Exception as e:
            print(f"Error segmenting image: {e}")
            return None

# Define filters and their descriptions
filters = {
    '1': {'name': 'Blur', 'description': 'Apply Gaussian blur to the image.'},
    '2': {'name': 'Rotate', 'description': 'Rotate the image by 180 degrees.'},
    '3': {'name': 'Salt and Pepper', 'description': 'Add salt-and-pepper noise to the image.'},
    '4': {'name': 'Concatenate', 'description': 'Concatenate the image with another image.'},
    '5': {'name': 'Segment', 'description': 'Segment the image using k-means clustering.'}
}

# Display available filters
print("Available filters:")
for key, value in filters.items():
    print(f"{key}. {value['name']}: {value['description']}")

# Get user input for filter and image file name
selected_filter = input("Enter the number of the filter you want to apply: ")
image_file = input("Enter the name of the image file (e.g., tiger.jpg): ")

image_path = os.path.join('images', image_file)

if selected_filter in filters:
    img_processor = Img(image_path)

    if selected_filter == '1':
        img_processor.blur()
    elif selected_filter == '2':
        img_processor.rotate()
    elif selected_filter == '3':
        img_processor.salt_n_pepper()
    elif selected_filter == '4':
        other_image_file = input("Enter the name of the other image file (e.g., cat.jpg): ")
        other_image_path = os.path.join('images', other_image_file)
        other_image_data = cv2.imread(other_image_path)
        if other_image_data is not None:
            img_processor.concat(other_image_data)
        else:
            print("Error: Unable to load the other image.")
    elif selected_filter == '5':
        img_processor.segment()
    else:
        print("Invalid filter number.")
else:
    print("Invalid filter number.")