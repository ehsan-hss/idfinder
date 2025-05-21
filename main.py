import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# فایل داده‌ها
DATA_FILE = "data.json"

# آیدی عددی ادمین (جایگزین کن)
ADMIN_ID = 5789565027

# تابع برای ذخیره داده
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# تابع برای خواندن داده
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_data()
    user_id = str(user.id)
    phone = user.phone_number if user.phone_number else "شماره‌ای ثبت نشده"

    if user_id not in data:
        data[user_id] = {
            "username": user.username,
            "name": f"{user.first_name} {user.last_name or ''}".strip(),
            "phone": phone
        }
        save_data(data)

    await update.message.reply_text("ثبت شد! خوش اومدی.")

# /getid <id>
async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if len(context.args) != 1:
        await update.message.reply_text("لطفاً آیدی عددی را وارد کن\nمثال: /getid 123456789")
        return

    query_id = context.args[0]
    if query_id in data:
        user_data = data[query_id]
        await update.message.reply_text(
            f"اطلاعات:\nنام: {user_data['name']}\nیوزرنیم: @{user_data['username']}\nشماره: {user_data['phone']}"
        )
    else:
        await update.message.reply_text("چنین آیدی‌ای پیدا نشد.")

# /list (فقط برای ادمین)
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("دسترسی نداری!")
        return

    data = load_data()
    if not data:
        await update.message.reply_text("لیست خالیه.")
        return

    msg = "لیست کاربران ثبت‌شده:\n"
    for uid, info in data.items():
        msg += f"آیدی: {uid} | نام: {info['name']} | شماره: {info['phone']}\n"
    
    await update.message.reply_text(msg[:4000])  # تا سقف تلگرام

app = ApplicationBuilder().token("7841546717:AAGXclNNdfQ_qQZaZKzS4oCm4rfDbl1jH1I").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getid", get_id))
app.add_handler(CommandHandler("list", list_users))

app.run_polling()
