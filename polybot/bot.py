import telebot
# import os
import cv2
from polybot.img_proc import Img

# Initialize your bot with your bot token
bot = telebot.TeleBot("6648578545:AAGj7wVJLGjMV6CYAPnEVGKH3MnbxpSs8uU")

# Dictionary to store the images temporarily
user_images = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Hello! Send me an image then choose a filter from the following options:\n"
                                      "- Blur\n"
                                      "- Rotate\n"
                                      "- Salt and Pepper\n"
                                      "- Segment")
# Define a handler for receiving photos
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        print("Received a photo message")
        # Get the photo file ID
        file_id = message.photo[-1].file_id
        # Get the file object using the file ID
        file_info = bot.get_file(file_id)
        # Download the file
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the file temporarily with a unique name based on the file ID
        image_path = f"images/{file_id}.jpg"
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Check if this is the first image or the second image for concatenation
        if message.chat.id in user_images:
            print("User already has an image in memory")
            if 'concat_pending' in user_images[message.chat.id]:
                print("This is the second image for concatenation")
                # This is the second image for concatenation
                second_image_path = image_path
                first_image_path = user_images[message.chat.id]['concat_pending']
                del user_images[message.chat.id]['concat_pending']  # Remove the pending flag

                # Load the images
                first_image_data = cv2.imread(first_image_path)
                second_image_data = cv2.imread(second_image_path)

                # Concatenate the images
                img_processor = Img(first_image_path)
                concatenated_image = img_processor.concat(second_image_data)
                if concatenated_image is not None:
                    print("Concatenation successful")
                    # Save and send the concatenated image
                    processed_image_path = img_processor.save_image(concatenated_image, suffix='_concatenated')
                    with open(processed_image_path, 'rb') as photo_file:
                        bot.send_photo(message.chat.id, photo_file)
                else:
                    print("Error concatenating images.")
                    bot.reply_to(message, "Error concatenating images.")

                # Clear user state
                del user_images[message.chat.id]
            else:
                # This is the first image
                print("This is the first image for concatenation")
                user_images[message.chat.id]['concat_pending'] = image_path
                bot.reply_to(message, "First image saved successfully! Now please send the second image to concatenate with.")
        else:
            # This is the first image
            print("This is the first image received")
            user_images[message.chat.id] = {'concat_pending': image_path}
            bot.reply_to(message, "First image saved successfully! Now to applay concat filter please send another image or choose a filter from the list in the top of the page to applay filter .")
    except Exception as e:
        print(f"Error handling image: {e}")
        bot.reply_to(message, f"Error handling image: {e}")
@bot.message_handler(func=lambda message: message.text.lower() in ['blur', 'rotate', 'salt and pepper', 'segment'])
def handle_filter(message):
    try:
        # Check if the user has previously sent an image
        if message.chat.id in user_images:
            # Get the image path
            if 'concat_pending' in user_images[message.chat.id]:
                image_path = user_images[message.chat.id]['concat_pending']
            else:
                image_path = user_images[message.chat.id]['first_image']

            # Apply the selected filter
            img_processor = Img(image_path)
            filter_name = message.text.lower()
            if filter_name == 'blur':
                processed_image = img_processor.blur()
            elif filter_name == 'rotate':
                processed_image = img_processor.rotate()
            elif filter_name == 'salt and pepper':
                processed_image = img_processor.salt_n_pepper()
            elif filter_name == 'segment':
                processed_image = img_processor.segment()

            else:
                processed_image = None

            # Check if the filter was applied successfully
            if processed_image is not None:
                # Save and send the processed image
                processed_image_path = img_processor.save_image(processed_image, suffix=f'{filter_name.replace(" ", "")}')
                with open(processed_image_path, 'rb') as photo_file:
                    bot.send_photo(message.chat.id, photo_file)
            else:
                bot.reply_to(message, f"Error applying {filter_name} filter: Result is None.")

            # Remove the image path from the dictionary
            del user_images[message.chat.id]
        else:
            bot.reply_to(message, "Please send an image first.")
    except Exception as e:
        bot.reply_to(message, f"Error processing image: {e}")

# Start your bot with polling
bot.polling()







# from dotenv import load_dotenv
# import telebot
# from polybot.img_proc import Img
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Initialize your bot with your bot token
# bot = telebot.TeleBot("6648578545:AAGj7wVJLGjMV6CYAPnEVGKH3MnbxpSs8uU")
#
# # Deactivate webhook (not necessary if you're using polling)
# bot.delete_webhook()
#
# # Define a handler for the /start command
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     bot.send_message(message.chat.id, "Hi, I'm Osherbot! Send me an image and choose a filter (blur, rotate, salt_n_pepper, segment).")
#
# # Define a handler for receiving photos
# @bot.message_handler(content_types=['photo'])
# def handle_image(message):
#     # Check if the message contains a photo
#     if message.photo:
#         # Get the photo file ID
#         file_id = message.photo[-1].file_id
#         # Get the file object using the file ID
#         file_info = bot.get_file(file_id)
#         # Download the file
#         downloaded_file = bot.download_file(file_info.file_path)
#
#         # Save the file temporarily with a unique name based on the file ID
#         with open(f"images/{file_id}.jpg", 'wb') as new_file:
#             new_file.write(downloaded_file)
#
#         # Reply to the user that the image was saved successfully
#         bot.reply_to(message, "Image saved successfully!")
#
#         # Get the selected filter from the message text (if available)
#         if message.caption:
#             selected_filter = message.caption.lower()
#         else:
#             bot.reply_to(message, "Please specify a filter (e.g., /blur, /rotate, /salt_n_pepper, /segment).")
#             return
#
#         # Load the saved image using Img
#         image_path = f"images/{file_id}.jpg"
#         img_processor = Img()  # Create an instance of Img
#         img_processor.load_image(image_path)  # Load the image from the file path
#
#         # Apply the selected filter based on user input
#         if selected_filter == 'blur':
#             img_processor.apply_blur()
#         elif selected_filter == 'rotate':
#             img_processor.apply_rotate()
#         elif selected_filter == 'salt_n_pepper':
#             img_processor.apply_salt_n_pepper()
#         elif selected_filter == 'segment':
#             img_processor.apply_segmentation()
#         elif selected_filter == 'concat':
#             img_processor.apply_concat()
#         else:
#             bot.reply_to(message, "Invalid filter. Please choose one of the supported filters: blur, rotate, salt_n_pepper, segment, concat")
#             return
#
#         # Save the processed image
#         img_processor.save_image(image_path)  # Overwrite the original image with the processed one
#
#         # Send back the processed image to the user
#         with open(image_path, 'rb') as photo_file:
#             bot.send_photo(message.chat.id, photo_file)
#     else:
#         bot.reply_to(message, "Please send a photo to apply the image processing.")
#
# # Start your bot with polling
# bot.polling()












# elif selected_filter == '/concat':
#     img_processor.apply_concat()

# from dotenv import load_dotenv
# import telebot
# from polybot.img_proc import Img
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Initialize your bot with your bot token
# bot = telebot.TeleBot("6648578545:AAGj7wVJLGjMV6CYAPnEVGKH3MnbxpSs8uU")
#
# # Deactivate webhook (not necessary if you're using polling)
# bot.delete_webhook()
#
# # Define a handler for the /start command
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     bot.send_message(message.chat.id, "Hi im Osherbot! Send me an image and I will process it.")
#
# # Define a handler for receiving photos
# @bot.message_handler(content_types=['photo'])
# def handle_image(message):
#     # Get the photo file ID
#     file_id = message.photo[-1].file_id
#     # Get the file object using the file ID
#     file_info = bot.get_file(file_id)
#     # Download the file
#     downloaded_file = bot.download_file(file_info.file_path)
#
#     # Save the file temporarily with a unique name based on the file ID
#     with open(f"images/{file_id}.jpg", 'wb') as new_file:
#         new_file.write(downloaded_file)
#
#     # Reply to the user that the image was saved successfully
#     bot.reply_to(message, "Image saved successfully!")
#
#     # Get the selected filter from the message caption
#     selected_filter = message.caption
#
#     # Load the saved image and apply the selected filter
#     image_path = f"images/{file_id}.jpg"
#     img_processor = Img(image_path)
#
#     if selected_filter == 'blur':
#         processed_image = img_processor.blur()
#     elif selected_filter == 'rotate':
#         processed_image = img_processor.rotate()
#     elif selected_filter == 'salt_n_pepper':
#         processed_image = img_processor.salt_n_pepper()
#     elif selected_filter == 'concat':
#         # Concatenation requires another image, handle it separately
#         processed_image = None
#     elif selected_filter == 'segment':
#         processed_image = img_processor.segment()
#     else:
#         bot.reply_to(message, "Invalid filter.")
#         return
#
#     # Check if image was processed successfully
#     if processed_image is not None:
#         # Save the processed image
#         img_processor.save_image(processed_image, suffix=f'_{selected_filter}')
#
#         # Send back the processed image to the user
#         with open(f"images/{file_id}_{selected_filter}.jpg", 'rb') as photo_file:
#             bot.send_photo(message.chat.id, photo_file)
#     else:
#         bot.reply_to(message, "Error processing image.")
#
# # Start your bot with polling
# bot.polling()













# from dotenv import load_dotenv
# import telebot
# from polybot.img_proc import Img
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Initialize your bot with your bot token
# bot = telebot.TeleBot("6648578545:AAGj7wVJLGjMV6CYAPnEVGKH3MnbxpSs8uU")
## # Deactivate webhook (not necessary if you're using polling)
# bot.delete_webhook()
#
#
# # Define a handler for the /start command
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     bot.send_message(message.chat.id, "Hi im Osherbot! Send me an image and I will process it.")
#
#
# # Define a handler for receiving photos
# @bot.message_handler(content_types=['photo'])
# def handle_image(message):
#     # Get the photo file ID
#     file_id = message.photo[-1].file_id
#     # Get the file object using the file ID
#     file_info = bot.get_file(file_id)
#     # Download the file
#     downloaded_file = bot.download_file(file_info.file_path)
#
#     # Save the file with a unique name based on the file ID
#     with open(f"images/{file_id}.jpg", 'wb') as new_file:
#         new_file.write(downloaded_file)
#
#     # Reply to the user that the image was saved successfully
#     bot.reply_to(message, "Image saved successfully!")
#
#     # Send the saved photo back to the user
#     with open(f"images/{file_id}.jpg", 'rb') as photo_file:
#         bot.send_photo(message.chat.id, photo_file)
#
#
# @bot.message_handler(commands=['blur'])
# def handle_blur(message):
#     process_image(message, Img.blur)
#
#
#
# # Define a handler for the /rotate command
# @bot.message_handler(commands=['rotate'])
# def handle_rotate(message):
#     process_image(message, Img.rotate)
#
#
# # Define a handler for the /salt_n_pepper command
# @bot.message_handler(commands=['salt_n_pepper'])
# def handle_salt_n_pepper(message):
#     process_image(message, Img.salt_n_pepper)
#
#
# # Define a handler for the /concat command
# @bot.message_handler(commands=['concat'])
# def handle_concat(message):
#     process_image(message, Img.concat)
#
#
# # Define a handler for the /segment command
# @bot.message_handler(commands=['segment'])
# def handle_segment(message):
#     process_image(message, Img.segment)
#
#
# # Function to process the received image using a specified image processing method
# def process_image(message, process_method):
#     # Check if the message contains a photo
#     if message.photo:
#         # Get the photo file ID
#         file_id = message.photo[-1].file_id
#
#         # Get the file object using the file ID
#         file_info = bot.get_file(file_id)
#
#         # Download the photo
#         downloaded_file = bot.download_file(file_info.file_path)
#
#         # Create an Img instance from the downloaded file
#         img = Img(downloaded_file)
#
#         # Apply the specified image processing method
#         processed_img = process_method(img)
#
#         # Save the processed image to a BytesIO object
#         processed_image_io = processed_img.save_to_bytesio()
#
#         # Reply to the user that the image was processed
#         bot.reply_to(message, "Image processed successfully!")
#
#         # Send the processed image back to the user
#         bot.send_photo(message.chat.id, processed_image_io)
#     else:
#         # If no photo is found in the message
#         bot.reply_to(message, "Please send a photo to apply the image processing.")
#
#
# # Start your bot with polling
# bot.polling()
