import os
import cv2
import numpy as np

class Img:
    def __init__(self, image_path):
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

            file_path = os.path.join(directory, f"{os.path.basename(self.image_path).split('.')[0]}{suffix}.jpg")
            cv2.imwrite(file_path, image_data)
            print(f"Image saved successfully: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def blur(self, blur_level=16):
        try:
            if self.image_data is None:
                raise ValueError("No image data available.")
            blur_level = max(1, blur_level)
            blur_level = blur_level + 1 if blur_level % 2 == 0 else blur_level
            blurred_image = cv2.GaussianBlur(self.image_data, (blur_level, blur_level), 0)
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

            # Convert segmented image back to BGR format
            segmented_image_bgr = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)

            # Darken the segmented image
            segmented_image_bgr = segmented_image_bgr * 0.5  # Reduce brightness by 50%

            return segmented_image_bgr
        except Exception as e:
            print(f"Error segmenting image: {e}")
            return None




# import cv2
# import numpy as np
#
# class Img:
#     def __init__(self):
#         self.image = None
#
#     def load_image(self, image_path):
#         self.image = cv2.imread(image_path)
#
#     def apply_blur(self):
#         if self.image is not None:
#             self.image = cv2.GaussianBlur(self.image, (9, 9), 2)
#
#     def apply_rotate(self):
#         if self.image is not None:
#             self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
#
#     def apply_salt_n_pepper(self, amount=0.05):
#         if self.image is not None:
#             noisy_image = np.zeros(self.image.shape, np.uint8)
#             threshold = 1 - amount
#             for i in range(self.image.shape[0]):
#                 for j in range(self.image.shape[1]):
#                     r = np.random.rand()
#                     if r < amount:
#                         noisy_image[i][j] = [0, 0, 0]  # Pepper (black)
#                     elif r > threshold:
#                         noisy_image[i][j] = [255, 255, 255]  # Salt (white)
#                     else:
#                         noisy_image[i][j] = self.image[i][j]
#             self.image = noisy_image
#
#     def apply_segmentation(self):
#         if self.image is not None:
#             print("Applying segmentation...")
#             # Convert the image to grayscale
#             gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
#
#             # Apply thresholding
#             _, segmented_image = cv2.threshold(gray_image, 255, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#             print("Segmentation applied successfully.")
#             return segmented_image
#         else:
#             print("No image data to apply segmentation.")
#             return None
#
#     def concat(self, other_image):
#         if self.image is not None and other_image is not None:
#             # Resize other_image to match the dimensions of self.image for concatenation
#             other_image_resized = cv2.resize(other_image, (self.image.shape[1], self.image.shape[0]))
#
#             # Concatenate horizontally (side by side)
#             self.image = np.concatenate((self.image, other_image_resized), axis=1)
#
#     def save_image(self, image_path):
#         if self.image is not None:
#             cv2.imwrite(image_path, self.image)
#
#




# # import os
# import cv2
# import numpy as np
#
# class Img:
#     def __init__(self):
#         self.image = None
#
#     def load_image(self, image_path):
#         self.image = cv2.imread(image_path)
#
#     def apply_blur(self):
#         if self.image is not None:
#             self.image = cv2.GaussianBlur(self.image, (9, 9), 2)
#
#     def apply_rotate(self):
#         if self.image is not None:
#             self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
#
#     def apply_salt_n_pepper(self, amount=0.05):
#         if self.image is not None:
#             noisy_image = self.image.copy()
#             mask = np.random.choice([0, 1, 2], size=self.image.shape[:2], p=[amount / 2, amount / 2, 1 - amount])
#             noisy_image[mask == 0] = 0  # Set 'salt' pixels (white)
#             noisy_image[mask == 1] = 255  # Set 'pepper' pixels (black)
#             self.image = noisy_image
#
#     def apply_segmentation(self):
#         if self.image is not None:
#             # Implement your image segmentation function here
#             # Example using simple thresholding
#             gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
#             _, segmented_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
#             return segmented_image
#
#     def concat(self, other_image):
#         if self.image is not None and other_image is not None:
#             # Resize other_image to match the dimensions of self.image for concatenation
#             other_image_resized = cv2.resize(other_image, (self.image.shape[1], self.image.shape[0]))
#
#             # Concatenate horizontally (side by side)
#             self.image = np.concatenate((self.image, other_image_resized), axis=1)
#
#     def save_image(self, image_path):
#         if self.image is not None:
#             cv2.imwrite(image_path, self.image)
#




#
# import os
# import cv2
# import numpy as np
#
# class Img:
#     def _init_(self, image_path):
#         self.image_path = image_path
#         self.image_data = self.load_image()
#
#     def load_image(self):
#         try:
#             image = cv2.imread(self.image_path)
#             if image is not None:
#                 return image
#             else:
#                 raise FileNotFoundError("Unable to load image.")
#         except Exception as e:
#             print(f"Error loading image: {e}")
#             return None
#
#     def save_image(self, image_data, suffix='_filtered'):
#         try:
#             directory = 'images'
#             if not os.path.exists(directory):
#                 os.makedirs(directory)
#
#             file_path = os.path.join(directory, f"{os.path.basename(self.image_path).split('.')[0]}{suffix}.jpg")
#             cv2.imwrite(file_path, image_data)
#             print(f"Image saved successfully: {file_path}")
#             return file_path
#         except Exception as e:
#             print(f"Error saving image: {e}")
#             return None
#
#     def blur(self, blur_level=16):
#         try:
#             if self.image_data is None:
#                 raise ValueError("No image data available.")
#             blur_level = max(1, blur_level)
#             blur_level = blur_level + 1 if blur_level % 2 == 0 else blur_level
#             blurred_image = cv2.GaussianBlur(self.image_data, (blur_level, blur_level), 0)
#             return blurred_image
#         except Exception as e:
#             print(f"Error applying blur: {e}")
#             return None
#
#     def rotate(self):
#         try:
#             img = cv2.imread(self.image_path)
#             if img is None:
#                 raise FileNotFoundError("Unable to load image.")
#             rotated_img = cv2.rotate(img, cv2.ROTATE_180)
#             return rotated_img
#         except Exception as e:
#             print(f"Error rotating image: {e}")
#             return None
#
#     def salt_n_pepper(self, amount=0.05):
#         try:
#             if self.image_data is None:
#                 raise ValueError("No image data available.")
#             noisy_image = self.image_data.copy()
#             mask = np.random.choice([0, 1, 2], size=noisy_image.shape[:2], p=[amount / 2, amount / 2, 1 - amount])
#             noisy_image[mask == 0] = 0
#             noisy_image[mask == 1] = 255
#             return noisy_image
#         except Exception as e:
#             print(f"Error adding salt and pepper noise: {e}")
#             return None
#
#     def concat(self, other_image_data, direction='horizontal'):
#         try:
#             if self.image_data is None or other_image_data is None:
#                 raise ValueError("Image data is missing.")
#             if direction not in ['horizontal', 'vertical']:
#                 raise ValueError("Invalid direction. Please use 'horizontal' or 'vertical'.")
#
#             if direction == 'horizontal':
#                 concatenated_img = np.concatenate((self.image_data, other_image_data), axis=2)
#             else:
#                 concatenated_img = np.concatenate((self.image_data, other_image_data), axis=1)
#             return concatenated_img
#         except Exception as e:
#             print(f"Error concatenating images: {e}")
#             return None
#
#     def segment(self, num_clusters=100):
#         try:
#             if self.image_data is None:
#                 raise ValueError("No image data available.")
#             image_rgb = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
#             pixels = image_rgb.reshape((-1, 3))
#             pixels = np.float32(pixels)
#             criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
#             _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
#             centers = np.uint8(centers)
#             segmented_image = centers[labels.flatten()]
#             segmented_image = segmented_image.reshape(image_rgb.shape)
#
#             # Darken the segmented image
#             segmented_image = segmented_image * 0.5  # Reduce brightness by 50%
#
#             return segmented_image
#         except Exception as e:
#             print(f"Error segmenting image: {e}")
#             return None







# from pathlib import Path
# import os
# from PIL import Image
# import cv2
# import numpy as np
#
#
# #
# class Img:
#     def __init__(self,image_path):
#         self.image_path = image_path
#         self.image_data = self.load_image()
#     # load image using cv2 if not return unable """"" if not loading return e (error)
#     def load_image(self):
#         try:
#             image = cv2.imread(self.image_path)
#             if image is not None:
#                 return image
#             else:
#                 raise FileNotFoundError("Unable to load image.")
#         except Exception as e:
#             print(f"Error loading image: {e}")
#             return None
#     #  save to directory images or os pathexists directory, add suffix use cv2 to rewrite object name or return
#     # saved successfully or e  error save img
#     def save_image(self, image_data, suffix='_filtered'):
#         try:
#             directory = 'images'
#             if not os.path.exists(directory):
#                 os.makedirs(directory)
#
#             path_obj = Path(self.image_path)
#             file_path = os.path.join(directory, "{}{}{}".format(path_obj.stem, suffix, path_obj.suffix))
#             cv2.imwrite(file_path, image_data)
#             print(f"Image saved successfully: {file_path}")
#         except Exception as e:
#             print(f"Error saving image: {e}")
#     #use "self" if there is no data available raise "ValueError",blur_level=16 useing % in to
#     #blur image, cv2 open n save  image data and self to save image and suffix and return blured image
#     #Exception e Error applying blur
#     def blur(self, blur_level=16):
#         try:
#             if self.image_data is None:
#                 raise ValueError("No image data available.")
#             blur_level = max(1, blur_level)
#             blur_level = blur_level + 1 if blur_level % 2 == 0 else blur_level
#             blurred_image = cv2.GaussianBlur(self.image_data, (blur_level, blur_level), 0)
#             self.save_image(blurred_image, '_blur')
#             return blurred_image
#         except Exception as e:
#             print(f"Error applying blur: {e}")
#             return None
#
#
#     def rotate(self):
#         try:
#             img = cv2.imread(self.image_path)
#             if img is None:
#                 raise FileNotFoundError("Unable to load image.")
#             rotated_img = cv2.rotate(img, cv2.ROTATE_180)
#             self.save_image(rotated_img, '_rotated')
#             return rotated_img
#         except Exception as e:
#             print(f"Error rotating image: {e}")
#             return None
#
#     def salt_n_pepper(self, amount=0.05):
#         try:
#             if self.image_data is None:
#                 raise ValueError("No image data available.")
#             noisy_image = self.image_data.copy()
#             mask = np.random.choice([0, 1, 2], size=noisy_image.shape[:2], p=[amount / 2, amount / 2, 1 - amount])
#             noisy_image[mask == 0] = 0
#             noisy_image[mask == 1] = 255
#             self.save_image(noisy_image, '_salt_n_pepper')
#             return noisy_image
#         except Exception as e:
#             print(f"Error adding salt and pepper noise: {e}")
#             return None
#     # use self or other image is none raise "" or if Invalid direction apllay np arrays 1 if horizontal 0 if vertical
#     #us self.save_img +suffix concatenated_img else Exception e error concatenating images
#     def concat(self, other_image_data, direction='horizontal'):
#         try:
#             if self.image_data is None or other_image_data is None:
#                 raise ValueError("Image data is missing.")
#             if direction not in ['horizontal', 'vertical']:
#                 raise ValueError("Invalid direction. Please use 'horizontal' or 'vertical'.")
#
#             if direction == 'horizontal':
#                 concatenated_img = np.concatenate((self.image_data, other_image_data), axis=1)
#             else:
#                 concatenated_img = np.concatenate((self.image_data, other_image_data), axis=0)
#             self.save_image(concatenated_img, '_concat')
#             return concatenated_img
#         except Exception as e:
#             print(f"Error concatenating images: {e}")
#             return None
#     #  chacking for data use image_rgb np cv2 to identify colors in img  and alter them
#     #  self.save_image to saave img+suffix else returb e error
#     def segment(self, num_clusters=100):
#         try:
#             if self.image_data is None:
#                 raise ValueError("No image data available.")
#             image_rgb = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
#             pixels = image_rgb.reshape((-1, 3))
#             pixels = np.float32(pixels)
#             criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
#             _, labels, centers = cv2.kmeans(pixels, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
#             centers = np.uint8(centers)
#             segmented_image = centers[labels.flatten()]
#             segmented_image = segmented_image.reshape(image_rgb.shape)
#
#             # Darken the segmented image
#             # Reduce brightness by 50%
#             segmented_image = segmented_image * 0.5
#
#             self.save_image(segmented_image, '_segment')
#             return segmented_image
#         except Exception as e:
#             print(f"Error segmenting image: {e}")
#             return None
#
# # Define filters and their descriptions
# filters = {
#     '1': {'name': 'Blur', 'description': 'Apply Gaussian blur to the image.'},
#     '2': {'name': 'Rotate', 'description': 'Rotate the image by 180 degrees.'},
#     '3': {'name': 'Salt and Pepper', 'description': 'Add salt-and-pepper noise to the image.'},
#     '4': {'name': 'Concatenate', 'description': 'Concatenate the image with another image.'},
#     '5': {'name': 'Segment', 'description': 'Segment the image using k-means clustering.'}
# }

# Display available filters
# print("Available filters:")
# for key, value in filters.items():
#     print(f"{key}. {value['name']}: {value['description']}")
#
# # Get user input for filter and image file name
# selected_filter = input("Enter the number of the filter you want to apply: ")
# image_file = input("Enter the name of the image file (e.g., tiger.jpg): ")
#
# image_path = os.path.join('images', image_file)
#
# if selected_filter in filters:
#     img_processor = Img(image_path)
#
#     if selected_filter == '1':
#         img_processor.blur()
#     elif selected_filter == '2':
#         img_processor.rotate()
#     elif selected_filter == '3':
#         img_processor.salt_n_pepper()
#     elif selected_filter == '4':
#         other_image_file = input("Enter the name of the other image file (e.g., cat.jpg): ")
#         other_image_path = os.path.join('images', other_image_file)
#         other_image_data = cv2.imread(other_image_path)
#         if other_image_data is not None:
#             img_processor.concat(other_image_data)
#         else:
#             print("Error: Unable to load the other image.")
#     elif selected_filter == '5':
#         img_processor.segment()
#     else:
#         print("Invalid filter number.")
# else:
#     print("Invalid filter number.")