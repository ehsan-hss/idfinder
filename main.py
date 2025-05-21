import telebot
from telebot import types

# جایگزین کن با توکن رباتت
TOKEN = "7841546717:AAGXclNNdfQ_qQZaZKzS4oCm4rfDbl1jH1I"

# جایگزین کن با آیدی عددی خودت (از @userinfobot بگیر)
ADMIN_ID = 5789565027

bot = telebot.TeleBot(TOKEN)

def save_number(username, phone):
    with open("data.txt", "a", encoding="utf-8") as f:
        f.write(f"{username}:{phone}\n")

def get_number(username):
    try:
        with open("data.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(username + ":"):
                    return line.split(":")[1].strip()
    except:
        return None
    return None

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    btn = types.KeyboardButton("ارسال یوزرنیم", request_contact=True)
    markup.add(btn)
    bot.send_message(message.chat.id, "وارد کردن ایدی تارگت بعد دکمه ارسال", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    if message.contact.user_id == message.from_user.id:
        username = message.from_user.username or f"id{message.from_user.id}"
        phone = message.contact.phone_number
        save_number(username, phone)
        bot.send_message(message.chat.id, "یوزرنیم ثبت شد ")
    else:
        bot.send_message(message.chat.id, "یوزرنیم ثبت نشد دوباره تلاش کنید")

@bot.message_handler(commands=['get'])
def get_user_number(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "شما اجازه این کار را ندارید.")
        return
    try:
        username = message.text.split()[1].replace("@", "")
        number = get_number(username)
        if number:
            bot.send_message(message.chat.id, f"شماره @{username}: {number}")
        else:
            bot.send_message(message.chat.id, "شماره‌ای برای این آیدی پیدا نشد.")
    except:
        bot.send_message(message.chat.id, "استفاده درست:\n/get @username")

bot.polling()
