import telebot
import requests
from flask import Flask
from threading import Thread

app = Flask('')

# توكن البوت من BotFather
TOKEN = '7445982313:AAHq9U8dcaMDLMe1F2dJntNmxr5U2THxxuY'
bot = telebot.TeleBot(TOKEN)

# قائمة بالمستخدمين المسموح لهم باستخدام البوت
ALLOWED_USERS = [7377632744 , 6853679072, 5460973447, 5052911838, 7095484110, 5078196107, 7395728648 ]  # ضع هنا معرفات المستخدمين المسموح لهم

# تخزين التوكنات للمستخدمين
user_tokens = {}

# دالة للتحقق من إذن المستخدم
def is_user_allowed(user_id):
    return user_id in ALLOWED_USERS

# دالة بدء المحادثة
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "عـذرا عزيزي انت  لاتمـلك الاذن لإستخدام البوت تواصل مـع المطـور 🧑🏻‍💻@abdoumihou2000")
        return

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    button1 = telebot.types.InlineKeyboardButton("📱إرســـال رقــــــمك يـــــــوز ", callback_data='send_phone')
    button2 = telebot.types.InlineKeyboardButton("إعادة تعـبئة بــــدون رمز ✨📨", callback_data='update_code')
    button3 = telebot.types.InlineKeyboardButton("عــــرض رصــــــيدك لحالــي🪪", callback_data='show_balance')
    keyboard.add(button1, button2, button3)

    welcome_message = f"""
♕أهلا بيـك يا‼️ {message.from_user.first_name} ‼️♕

♡‼️𝘼𝘽𝘿𝙊𝙐 𝙔𝙊𝙊𝙕 𝙑𝙄𝙋‼️♡

♕‼️خـير وحدة من هاذ لعــروض لي تناسبك ‼️♕
"""
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

# دالة لمعالجة الرقم المدخل
def handle_number(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "عـذرا عزيزي انت  لاتمـلك الاذن لإستخدام البوت تواصل مـع المطـور 🧑🏻‍💻@abdoumihou2000 ")
        return

    num = message.text
    bot.send_message(message.chat.id, 'يتم التحقق من رقم هاتفك سيتم ارسال رمز تحقق🔍')

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3',
    }

    data = {
        'client_id': 'ibiza-app',
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    if 'ROOGY' in response.text:
        bot.send_message(message.chat.id, 'تـم ارسـال رمـز تحقق قم بـإرساله من فضلك📨🧾')
        bot.send_message(message.chat.id, '💬')
    else:
        bot.send_message(message.chat.id, 'حـذث خطأ اثـناء ارسال الرمز يـرجى اعادة المحاولة بعد دقيقتين ‼️')

    bot.register_next_step_handler(message, handle_otp, num)

# دالة لمعالجة الكود المدخل
def handle_otp(message, num):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "عـذرا عزيزي انت  لاتمـلك الاذن لإستخدام البوت تواصل مـع المطـور 🧑🏻‍💻@abdoumihou2000")
        return

    otp = message.text

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ibiza.ooredoo.dz',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp',
    }

    data = {
        'client_id': 'ibiza-app',
        'otp': otp,
        'grant_type': 'password',
        'mobile-number': num,
        'language': 'AR',
    }

    response = requests.post('https://ibiza.ooredoo.dz/auth/realms/ibiza/protocol/openid-connect/token', headers=headers, data=data)
    access_token = response.json().get('access_token')

    if access_token:
        user_tokens[message.from_user.id] = access_token
        bot.send_message(message.chat.id, 'تم التحقق بنجاح  يتم ارسال الانترنت.......... 🪅')
        send_internet(message, access_token)
    else:
        bot.send_message(message.chat.id, 'عذرا هناك خطأ في التاكد من رمز تحقق يرجى اعادة المحاولة لاحقا ‼️')

# دالة للتحقق من حجم الانترنت
def check_internet_volume(access_token):
    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/balance'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    volume = response.json().get('accounts', [{}])[1].get('value', 'غير متاح')
    return volume

# دالة لإرسال الانترنت
def send_internet(message, access_token):
    url = 'https://ibiza.ooredoo.dz/api/v1/mobile-bff/users/mgm/info/apply'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'language': 'AR',
        'request-id': 'ef69f4c6-2ead-4b93-95df-106ef37feefd',
        'flavour-type': 'gms',
        'Content-Type': 'application/json'
    }

    payload = {
        "mgmValue": "ABC"
    }

    # التحقق من حجم الانترنت قبل تطبيق التوكن
    initial_volume = check_internet_volume(access_token)
    bot.send_message(message.chat.id, f'⊢――――اصـبر شويا من فضلك―――――⊣\n『 حـجـم الأنـترنت تاعـك قبـل مترسـل :{initial_volume} 🪪\n┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄』\n﴿ملاحظة مهمة : يمكنك التسجيل مرة واحدة كل 2 دقائق ⌛﴾')

    for _ in range(10):
        response = requests.post(url, headers=headers, json=payload).text
        if 'Request Rejecte' not in response:
            pass
        else:
            final_volume = check_internet_volume(access_token)
            bot.send_message(message.chat.id, f'┏══════ 🎁 ═══════╗\n✯✯𝘼𝘽𝘿𝙊𝙐 𝙔𝙊𝙊𝙕 𝙑𝙄𝙋✯✯\n𓊈{final_volume} 🎉𓊉              حجم أنترنت بعد إرسال 🎊\n┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄\n✅صالحــــــة لمدة: 7 أيامــ  📅\n\n✅ المطور  :@abdoumihou2000🇮🇹')
            break
    else:
        bot.send_message(message.chat.id, '')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'send_phone':
        bot.send_message(call.message.chat.id, '🪽أرســــــل رقـمك مــــن فضــــــلك 🪽')
        bot.register_next_step_handler(call.message, handle_number)
    elif call.data == 'update_code':
        if call.from_user.id in user_tokens:
            bot.send_message(call.message.chat.id, 'تـتم تعــــــبئة🧃......... ')
            send_internet(call.message, user_tokens[call.from_user.id])
        else:
            bot.send_message(call.message.chat.id, 'عذرا!، رقمك ليـس محـفوض، رجاء قيام بعملية تسجيل لكي تقوم بعملية هذه  ♡')
    elif call.data == 'show_balance':
        if call.from_user.id in user_tokens:
            volume = check_internet_volume(user_tokens[call.from_user.id])
            bot.send_message(call.message.chat.id, f'رصـــــــيدك حالـي♕ 🪪: {volume}')
        else:
            bot.send_message(call.message.chat.id, 'عذرا!، رقمك ليـس محـفوض، رجاء قيام بعملية تسجيل لكي تقوم بعملية هذه  ♡')

# بدء البوت
@app.route('/')
def home():
    return "<b>telegram @X0_XV</b>"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending=True)