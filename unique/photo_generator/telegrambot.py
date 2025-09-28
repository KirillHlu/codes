import telebot
import time
from test import *
from telebot import types


def create_design_function(users_room, promt_from_user):
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', '2948185B516F87FF7ACC7C372FD6F395',
                         '31F11AFFD2CBD8CBF83D371CDAB5F505')
    try:
        pipeline_id = api.get_pipeline()
        print(f"Pipeline ID: {pipeline_id}")

        uuid = api.generate(f"create a design for {users_room}: {promt_from_user}", pipeline_id)
        print(f"Request UUID: {uuid}")

        files = api.check_generation(uuid)

        if files:
            # Create filename with timestamp
            timestamp = int(time.time())
            filename = f"generated_image_{timestamp}.png"

            # Save the image
            saved_file = api.save_image(files, filename)

            if saved_file:
                print(f"Image successfully saved: {saved_file}")
                return saved_file  # Return the file path, not the files data
            else:
                print("Failed to save image")
                return None
        else:
            print("Failed to get image")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


API_TOKEN = "8370523593:AAG34Z4qw0xUNlEJ6auFTyfTG0Itp6OVR1E"

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     'Hello, it is a bot to create design of your rooms.\nSend me /create "type of room" "description" to create the design.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("help")
    markup.add(btn1)

@bot.message_handler(commands=['help'])
def help1(message):
    bot.send_message(message.chat.id, 'Send me /create "type of room" "description" to create the design.')

@bot.message_handler(commands=['create'])
def create_design(message):
    parts_of_messages = str(message.text).split(" ")
    if len(parts_of_messages) < 3:
        bot.send_message(message.chat.id, "Please use format: /create 'type_of_room' 'description'")
        return

    type_of_room = parts_of_messages[1]
    description = ' '.join(parts_of_messages[2:])

    bot.send_message(message.chat.id, f"Creating design for {type_of_room}: {description}")

    image_path = create_design_function(type_of_room, description)

    with open(image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.polling(True)
