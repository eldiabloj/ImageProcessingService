import os
import telebot
import cv2
from img_proc import Img
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    print("Error: TELEGRAM_TOKEN is not set in the .env file.")
    exit(1)

# Initialize the Telegram bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Dictionary to store temporary user data
user_images = {}

# Helper function to save images
def save_image(file_path, file_data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as new_file:
        new_file.write(file_data)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, (
        "Welcome to the Image Processing Bot! 🎉\n"
        "You can send me an image and apply various filters or concatenate images.\n"
        "Available filters: Blur, Rotate, Salt and Pepper, Segment, Convert to Grayscale, Adjust.\n"
        "Steps:\n"
        "1. Send your first image.\n"
        "2. Optionally, send a second image for concatenation.\n"
        "3. Choose a filter from the list."
    ))

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    try:
        user_id = message.chat.id
        user_dir = f"images/{user_id}"
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_data = bot.download_file(file_info.file_path)
        image_path = os.path.join(user_dir, f"{file_id}.jpg")
        save_image(image_path, file_data)

        if user_id in user_images and 'concat_pending' in user_images[user_id]:
            first_image_path = user_images[user_id]['concat_pending']
            second_image_path = image_path
            del user_images[user_id]['concat_pending']

            first_img = cv2.imread(first_image_path)
            second_img = cv2.imread(second_image_path)

            img_processor = Img(first_image_path)
            result = img_processor.concat(second_img)

            if result is not None:
                result_path = img_processor.save_image(result, suffix='_concatenated')
                with open(result_path, 'rb') as photo_file:
                    bot.send_photo(user_id, photo_file)
            else:
                bot.reply_to(message, "Error concatenating images.")
        else:
            user_images[user_id] = {'concat_pending': image_path}
            bot.reply_to(message, "First image saved! Send another image for concatenation or choose a filter.")
    except Exception as e:
        bot.reply_to(message, f"Error processing the image: {e}")

@bot.message_handler(func=lambda msg: msg.text.lower() in ['blur', 'rotate', 'salt and pepper', 'segment', 'convert to grayscale', 'adjust'])
def apply_filter(message):
    try:
        user_id = message.chat.id
        if user_id not in user_images or 'concat_pending' not in user_images[user_id]:
            bot.reply_to(message, "Please send an image first.")
            return

        image_path = user_images[user_id]['concat_pending']
        img_processor = Img(image_path)
        filters = {
            'blur': img_processor.blur,
            'rotate': img_processor.rotate,
            'salt and pepper': img_processor.salt_n_pepper,
            'segment': img_processor.segment,
            'convert to grayscale': img_processor.convert_to_grayscale,
            'adjust': img_processor.adjust_brightness,
        }

        filter_func = filters.get(message.text.lower())
        if filter_func:
            result = filter_func()
            if result is not None:
                result_path = img_processor.save_image(result, suffix=f"_{message.text.replace(' ', '_')}")
                with open(result_path, 'rb') as photo_file:
                    bot.send_photo(user_id, photo_file)
            else:
                bot.reply_to(message, f"Error applying the {message.text} filter.")
        else:
            bot.reply_to(message, "Invalid filter. Please choose a valid option.")
    except Exception as e:
        bot.reply_to(message, f"Error processing the filter: {e}")

print("Bot is running...")
bot.polling()















# import os
# import telebot
# import cv2
# from img_proc import Img
# from dotenv import load_dotenv
#
#
#
#
#
# load_dotenv()
# TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
#
# # Check if TELEGRAM_TOKEN is not none
# if TELEGRAM_TOKEN is None:
#     print("Error: TELEGRAM_TOKEN is not set in the ..env file.")
#     exit(1)
#
# # initialize TELEGRAM_BOT
# bot = telebot.TeleBot(TELEGRAM_TOKEN)
#
#
# # Dictionary to store the images temporarily
# user_images = {}
#
# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     bot.send_message(message.chat.id, "Hi there! Send me an image then choose a filter from the following options:\n"
#                                       "- Blur\n"
#                                       "- Rotate\n"
#                                       "- Salt and Pepper\n"
#                                       "- Segment\n"
#                                       "- convert to grayscale\n"
#                                       "- adjust")
# # Define a handler for receiving photos
# @bot.message_handler(content_types=['photo'])
# def handle_image(message):
#     try:
#         print("Received a photo message")
#         # Get the photo file ID
#         file_id = message.photo[-1].file_id
#         # Get the file object using the file ID
#         file_info = bot.get_file(file_id)
#         # Download the file
#         downloaded_file = bot.download_file(file_info.file_path)
#
#         # Save the file temporarily with a unique name based on the file ID
#         image_path = f"images/{file_id}.jpg"
#         with open(image_path, 'wb') as new_file:
#             new_file.write(downloaded_file)
#
#         # Check if this is the first image or the second image for concatenation
#         if message.chat.id in user_images:
#             print("User already has an image in memory")
#             if 'concat_pending' in user_images[message.chat.id]:
#                 print("This is the second image for concatenation")
#                 # This is the second image for concatenation
#                 second_image_path = image_path
#                 first_image_path = user_images[message.chat.id]['concat_pending']
#                 del user_images[message.chat.id]['concat_pending']  # Remove the pending flag
#
#                 # Load the images
#                 first_image_data = cv2.imread(first_image_path)
#                 second_image_data = cv2.imread(second_image_path)
#
#                 # Concatenate the images
#                 img_processor = Img(first_image_path)
#                 concatenated_image = img_processor.concat(second_image_data)
#                 if concatenated_image is not None:
#                     print("Concatenation successful")
#                     # Save and send the concatenated image
#                     processed_image_path = img_processor.save_image(concatenated_image, suffix='_concatenated')
#                     with open(processed_image_path, 'rb') as photo_file:
#                         bot.send_photo(message.chat.id, photo_file)
#                 else:
#                     print("Error concatenating images.")
#                     bot.reply_to(message, "Error concatenating images.")
#
#                 # Clear user
#                 del user_images[message.chat.id]
#             else:
#                 # This is the first image
#                 print("This is the first image for concatenation")
#                 user_images[message.chat.id]['concat_pending'] = image_path
#                 bot.reply_to(message, "First image saved successfully! Now please send the second image to concatenate with.")
#         else:
#             # This is the first image+ the choose filter op's
#             print("This is the first image received")
#             user_images[message.chat.id] = {'concat_pending': image_path}
#             bot.reply_to(message, "First image saved successfully! Now to applay concat  filter please send another image or choose a filter from the list \n"
#                                       "- Blur\n"
#                                       "- Rotate\n"
#                                       "- Salt and Pepper\n"
#                                       "- Segment\n"
#                                       "- convert to grayscale\n"
#                                       "- adjust")
#     except Exception as e:
#         print(f"Error handling image: {e}")
#         bot.reply_to(message, f"Error handling image: {e}")
# @bot.message_handler(func=lambda message: message.text.lower() in ['blur', 'rotate', 'salt and pepper', 'segment', 'convert to grayscale', 'adjust'])
# def handle_filter(message):
#     try:
#         # Check if the user has previously sent an image
#         if message.chat.id in user_images:
#             # Get the image path
#             if 'concat_pending' in user_images[message.chat.id]:
#                 image_path = user_images[message.chat.id]['concat_pending']
#             else:
#                 image_path = user_images[message.chat.id]['first_image']
#
#             # Apply the selected filter
#             img_processor = Img(image_path)
#             filter_name = message.text.lower()
#             if filter_name == 'blur':
#                 processed_image = img_processor.blur()
#             elif filter_name == 'rotate':
#                 processed_image = img_processor.rotate()
#             elif filter_name == 'salt and pepper':
#                 processed_image = img_processor.salt_n_pepper()
#             elif filter_name == 'segment':
#                 processed_image = img_processor.segment()
#             elif filter_name == 'convert to grayscale':
#                 processed_image = img_processor.convert_to_grayscale()
#             elif filter_name == 'adjust':
#                 processed_image = img_processor.adjust_brightness()
#             else:
#                 processed_image = None
#
#             # Check if the filter was applied successfully
#             if processed_image is not None:
#                 # Save and send the processed image
#                 processed_image_path = img_processor.save_image(processed_image, suffix=f'{filter_name.replace(" ", "")}')
#                 with open(processed_image_path, 'rb') as photo_file:
#                     bot.send_photo(message.chat.id, photo_file)
#             else:
#                 bot.reply_to(message, f"Error applying {filter_name} filter: Result is None.")
#
#             # Remove the image path from the dictionary
#             del user_images[message.chat.id]
#         else:
#             bot.reply_to(message, "Please send an image first.")
#     except Exception as e:
#         bot.reply_to(message, f"Error processing image: {e}")
#
# # Start your bot with polling +running or not
# try:
#     print("Bot is running...")
#     bot.polling()
# except Exception as e:
#     print(f"Error starting bot: {e}")