# not in use



# import flask
# from flask import request
# import os
# from bot import Bot, QuoteBot, ImageProcessingBot
#
# os.environ['TELEGRAM_TOKEN'] ='6648578545:AAGj7wVJLGjMV6CYAPnEVGKH3MnbxpSs8uU'
# os.environ['TELEGRAM_APP_URL'] ='https://t.me/Eldiablojbot'
# app = flask.Flask(__name__)
#
# TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
# TELEGRAM_APP_URL = os.environ["TELEGRAM_APP_URL"]
#
#
# @app.route('/', methods=['GET'])
# def index():
#     return 'Ok'
#
#
# @app.route(f'/{TELEGRAM_TOKEN}/', methods=['POST'])
# def webhook():
#     req = request.get_json()
#     bot.handle_message(req['message'])
#     return 'Ok'
#
#
# if __name__ == "__main__":
#     bot = ImageProcessingBot(TELEGRAM_TOKEN, TELEGRAM_APP_URL)
#
#     app.run(host='0.0.0.0', port=8443)
