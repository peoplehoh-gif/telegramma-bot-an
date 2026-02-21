import telebot
from telebot import types

# ================= НАСТРОЙКИ =================
TOKEN = "8501484210:AAHLackjXS5JboBTz8VEouI-koZbV6uDQuw"
ADMIN_ID = 7939301679  # ← твой chat_id (число)
# =============================================

bot = telebot.TeleBot(TOKEN)

waiting_users = []
vip_waiting = []
active_chats = {}
all_users = set()
banned_users = set()
vip_users = set()
bot_enabled = True

# ================= КЛАВИАТУРЫ =================
def main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔎 Найти собеседника")
    markup.add("❌ Остановить чат")
    markup.add("🚫 Пожаловаться")
    if user_id == ADMIN_ID:
        markup.add("👑 Админ панель")
    return markup

def admin_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Статистика")
    markup.add("📢 Рассылка")
    markup.add("🚫 Бан")
    markup.add("♻ Разбан")
    markup.add("👑 Выдать VIP")
    markup.add("❌ Удалить VIP")
    markup.add("📃 Активные чаты")
    markup.add("🧹 Очистить очередь")
    markup.add("🛑 Выключить бота")
    markup.add("▶ Включить бота")
    markup.add("⬅ Назад")
    return markup

# ================= СТАРТ =================
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    all_users.add(user_id)

    if user_id in banned_users:
        bot.send_message(user_id, "🚫 Ты заблокирован.")
        return

    bot.send_message(user_id,
        "🎥 PRO Анонимная рулетка для ютуберов\nVIP получают приоритет 🔥",
        reply_markup=main_menu(user_id))

# ================= АДМИН ПАНЕЛЬ =================
@bot.message_handler(func=lambda m: m.text == "👑 Админ панель")
def open_admin(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "👑 PRO Админ панель", reply_markup=admin_menu())

@bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def stats(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id,
            f"👥 Всего: {len(all_users)}\n"
            f"💬 Чаты: {len(active_chats)//2}\n"
            f"👑 VIP: {len(vip_users)}\n"
            f"🚫 Забанено: {len(banned_users)}")

@bot.message_handler(func=lambda m: m.text == "🧹 Очистить очередь")
def clear_queue(message):
    if message.chat.id == ADMIN_ID:
        waiting_users.clear()
        vip_waiting.clear()
        bot.send_message(message.chat.id, "Очередь очищена.")

@bot.message_handler(func=lambda m: m.text == "🛑 Выключить бота")
def disable_bot(message):
    global bot_enabled
    if message.chat.id == ADMIN_ID:
        bot_enabled = False
        bot.send_message(message.chat.id, "Бот выключен.")

@bot.message_handler(func=lambda m: m.text == "▶ Включить бота")
def enable_bot(message):
    global bot_enabled
    if message.chat.id == ADMIN_ID:
        bot_enabled = True
        bot.send_message(message.chat.id, "Бот включён.")

@bot.message_handler(func=lambda m: m.text == "🚫 Бан")
def ban_request(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Введи ID пользователя для бана:")
        bot.register_next_step_handler(msg, ban_user)

def ban_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text)
            banned_users.add(user_id)
            bot.send_message(message.chat.id, "✅ Пользователь забанен.")
        except:
            bot.send_message(message.chat.id, "Ошибка ID.")

@bot.message_handler(func=lambda m: m.text == "♻ Разбан")
def unban_request(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Введи ID пользователя для разбанa:")
        bot.register_next_step_handler(msg, unban_user)

def unban_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text)
            banned_users.discard(user_id)
            bot.send_message(message.chat.id, "✅ Пользователь разбанен.")
        except:
            bot.send_message(message.chat.id, "Ошибка ID.")

@bot.message_handler(func=lambda m: m.text == "👑 Выдать VIP")
def vip_request(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Введи ID пользователя для VIP:")
        bot.register_next_step_handler(msg, give_vip)

def give_vip(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text)
            vip_users.add(user_id)
            bot.send_message(message.chat.id, "✅ VIP выдан.")
        except:
            bot.send_message(message.chat.id, "Ошибка ID.")

@bot.message_handler(func=lambda m: m.text == "❌ Удалить VIP")
def remove_vip_request(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Введи ID пользователя для удаления VIP:")
        bot.register_next_step_handler(msg, remove_vip)

def remove_vip(message):
    if message.chat.id == ADMIN_ID:
        try:
            user_id = int(message.text)
            vip_users.discard(user_id)
            bot.send_message(message.chat.id, "✅ VIP удален.")
        except:
            bot.send_message(message.chat.id, "Ошибка ID.")

@bot.message_handler(func=lambda m: m.text == "📃 Активные чаты")
def active_list(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, str(active_chats))

@bot.message_handler(func=lambda m: m.text == "📢 Рассылка")
def broadcast_request(message):
    if message.chat.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Введи текст для рассылки:")
        bot.register_next_step_handler(msg, broadcast_send)

def broadcast_send(message):
    if message.chat.id == ADMIN_ID:
        for user in all_users:
            try:
                bot.send_message(user, f"📢 Сообщение от админа:\n\n{message.text}")
            except:
                pass
        bot.send_message(message.chat.id, "✅ Рассылка завершена.")

@bot.message_handler(func=lambda m: m.text == "⬅ Назад")
def back(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Главное меню", reply_markup=main_menu(message.chat.id))

# ================= ПОИСК И ЧАТ =================
@bot.message_handler(func=lambda m: m.text == "🔎 Найти собеседника")
def find_partner(message):
    global bot_enabled
    user_id = message.chat.id

    if not bot_enabled:
        bot.send_message(user_id, "⚠ Бот временно отключён.")
        return

    if user_id in banned_users:
        return

    if user_id in active_chats:
        bot.send_message(user_id, "Ты уже в чате.")
        return

    queue = vip_waiting if user_id in vip_users else waiting_users

    if user_id in vip_users and vip_waiting:
        partner_id = vip_waiting.pop(0)
    elif vip_waiting:
        partner_id = vip_waiting.pop(0)
    elif waiting_users:
        partner_id = waiting_users.pop(0)
    else:
        queue.append(user_id)
        bot.send_message(user_id, "⏳ Поиск собеседника...")
        return

    active_chats[user_id] = partner_id
    active_chats[partner_id] = user_id

    bot.send_message(user_id, "✅ Собеседник найден!", reply_markup=main_menu(user_id))
    bot.send_message(partner_id, "✅ Собеседник найден!", reply_markup=main_menu(partner_id))

@bot.message_handler(func=lambda m: m.text == "❌ Остановить чат")
def stop_chat(message):
    user_id = message.chat.id
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        del active_chats[user_id]
        del active_chats[partner_id]
        bot.send_message(user_id, "❌ Чат завершён.", reply_markup=main_menu(user_id))
        bot.send_message(partner_id, "❌ Собеседник вышел.", reply_markup=main_menu(partner_id))

@bot.message_handler(func=lambda m: m.text == "🚫 Пожаловаться")
def report_user(message):
    user_id = message.chat.id
    if user_id in active_chats:
        partner_id = active_chats[user_id]
        bot.send_message(ADMIN_ID, f"🚨 Жалоба!\nОт: {user_id}\nНа: {partner_id}")
        bot.send_message(user_id, "Жалоба отправлена администратору.")

# ================= RELAY (только для чата, после всех кнопок) =================
@bot.message_handler(content_types=['text','photo','voice'])
def relay(message):
    user_id = message.chat.id

    if user_id in active_chats:
        partner_id = active_chats[user_id]
        try:
            if message.content_type == 'text':
                bot.send_message(partner_id, message.text)
            elif message.content_type == 'photo':
                bot.send_photo(partner_id, message.photo[-1].file_id)
            elif message.content_type == 'voice':
                bot.send_voice(partner_id, message.voice.file_id)
        except:
            pass

# ================= ЗАПУСК =================
print("PRO бот запущен...")
bot.infinity_polling()