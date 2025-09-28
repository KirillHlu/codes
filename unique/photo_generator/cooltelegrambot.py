import telebot
import time
import os
from test import *
from telebot import types

API_TOKEN = "8370523593:AAG34Z4qw0xUNlEJ6auFTyfTG0Itp6OVR1E"
bot = telebot.TeleBot(API_TOKEN)

user_states = {}


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
            timestamp = int(time.time())
            filename = f"generated_image_{timestamp}.png"

            saved_file = api.save_image(files, filename)

            if saved_file:
                print(f"Image successfully saved: {saved_file}")
                return saved_file
            else:
                print("Failed to save image")
                return None
        else:
            print("Failed to get image")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def create_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_create = types.KeyboardButton("🎨 Создать дизайн")
    btn_help = types.KeyboardButton("❓ Помощь")
    btn_examples = types.KeyboardButton("📋 Примеры комнат")
    markup.add(btn_create, btn_help, btn_examples)
    return markup


def create_cancel_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cancel = types.KeyboardButton("❌ Отмена")
    markup.add(btn_cancel)
    return markup


def create_room_types_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    rooms = ["Гостиная", "Спальня", "Кухня", "Ванная", "Кабинет", "Детская", "Прихожая", "Балкон"]
    buttons = [types.KeyboardButton(room) for room in rooms]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("❌ Отмена"))
    return markup


@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = """
🏠 Добро пожаловать в бот для создания дизайна комнат!

Я помогу вам создать уникальный дизайн для любой комнаты. 

Для начала работы нажмите кнопку "🎨 Создать дизайн" или воспользуйтесь командой /create
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_main_keyboard())


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📖 **Как пользоваться ботом:**

1. Нажмите "🎨 Создать дизайн"
2. Выберите тип комнаты из списка или введите свой
3. Опишите желаемый дизайн (стиль, цвета, мебель и т.д.)
4. Дождитесь генерации изображения

📝 **Примеры описания:**
- "Современная гостиная в светлых тонах с большим диваном и телевизором"
- "Минималистичная спальня с деревянной мебелью и мягким освещением"
- "Яркая детская комната с игровой зоной и тематическими обоями"

💡 **Совет:** Чем подробнее описание, тем лучше результат!
    """
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', reply_markup=create_main_keyboard())


@bot.message_handler(commands=['create'])
def create_design_command(message):
    start_design_process(message.chat.id)


def start_design_process(chat_id):
    user_states[chat_id] = {'step': 'waiting_room_type'}
    bot.send_message(chat_id,
                     "🏠 Выберите тип комнаты из списка или введите свой:",
                     reply_markup=create_room_types_keyboard())


@bot.message_handler(func=lambda message: message.text == "🎨 Создать дизайн")
def create_design_button(message):
    start_design_process(message.chat.id)


@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def help_button(message):
    help_command(message)


@bot.message_handler(func=lambda message: message.text == "📋 Примеры комнат")
def examples_button(message):
    examples_text = """
📋 **Примеры типов комнат и описаний:**

🏠 **Гостиная:**
   - "Современная гостиная в стиле лофт с кирпичной стеной"
   - "Классическая гостиная с камином и мягкими креслами"

🛏️ **Спальня:**
   - "Уютная спальня в скандинавском стиле с пастельными тонами"
   - "Роскошная спальня с большой кроватью и гардеробной"

🍳 **Кухня:**
   - "Современная кухня с островом и барными стульями"
   - "Деревенская кухня в стиле прованс"

🛁 **Ванная:**
   - "Современная ванная комната с джакуззи и стеклянной душевой"
   - "Минималистичная ванная с деревянными акцентами"
    """
    bot.send_message(message.chat.id, examples_text, parse_mode='Markdown')


@bot.message_handler(func=lambda message: message.text == "❌ Отмена")
def cancel_button(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id,
                     "❌ Процесс отменен. Что хотите сделать дальше?",
                     reply_markup=create_main_keyboard())


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    user_state = user_states.get(chat_id, {})

    if user_state.get('step') == 'waiting_room_type':
        user_states[chat_id] = {
            'step': 'waiting_description',
            'room_type': message.text
        }
        bot.send_message(chat_id,
                         f"🏠 Вы выбрали: {message.text}\n\n"
                         f"📝 Теперь опишите желаемый дизайн:\n"
                         f"(стиль, цвета, мебель, освещение и т.д.)",
                         reply_markup=create_cancel_keyboard())

    elif user_state.get('step') == 'waiting_description':
        room_type = user_state['room_type']
        description = message.text

        user_states.pop(chat_id, None)

        processing_msg = bot.send_message(chat_id,
                                          "⏳ Генерирую дизайн... Это может занять несколько минут.",
                                          reply_markup=types.ReplyKeyboardRemove())

        try:
            image_path = create_design_function(room_type, description)

            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as photo:
                    bot.send_photo(chat_id, photo,
                                   caption=f"🎨 Готовый дизайн для {room_type}!\n"
                                           f"📝 Ваше описание: {description}")

                bot.delete_message(chat_id, processing_msg.message_id)

                markup = types.InlineKeyboardMarkup()
                btn_new_design = types.InlineKeyboardButton("🔄 Создать еще один дизайн", callback_data="new_design")
                markup.add(btn_new_design)

                bot.send_message(chat_id,
                                 "Хотите создать еще один дизайн?",
                                 reply_markup=markup)
                try:
                    os.remove(image_path)
                except:
                    pass
            else:
                bot.edit_message_text("❌ Произошла ошибка при генерации изображения. Попробуйте еще раз.",
                                      chat_id, processing_msg.message_id)
                bot.send_message(chat_id, "Что хотите сделать дальше?", reply_markup=create_main_keyboard())

        except Exception as e:
            print(f"Error in design generation: {e}")
            bot.edit_message_text("❌ Произошла ошибка. Попробуйте еще раз.",
                                  chat_id, processing_msg.message_id)
            bot.send_message(chat_id, "Что хотите сделать дальше?", reply_markup=create_main_keyboard())

    else:
        # Сообщение не в процессе создания дизайна
        bot.send_message(chat_id,
                         "Я не понял ваше сообщение. Используйте кнопки ниже или команду /help для справки.",
                         reply_markup=create_main_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "new_design":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        start_design_process(call.message.chat.id)


if __name__ == "__main__":
    print("Бот запущен...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(15)
