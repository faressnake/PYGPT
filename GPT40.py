from langdetect import detect
from datetime import datetime
from telebot import types
from gtts import gTTS
import requests
import telebot
import sqlite3
import json
import os
import string

def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation + '؟،؛!'))
    return text.strip()
ze = '7732602872:AAEJHiFKo7XNH8wrVom7Oicg_5My0P58gQs' #توكنك 
ch = 'tech619info'
ADMIN = [5179688953, 0]
us = 'Hellyeah619' #يوزرك من دون @
vipcode_max = 4000 #عد احرف الرساله
#2021 
API_URL = 'https://baithek.com/chatbee/health_ai/ai_vision.php'
#2023 احذف الفوق لو عايزها 
#API_URL = 'https://baithek.com/chatbee/health_ai/ai_vision.php'
zo = telebot.TeleBot(ze)

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @B_Y_B_Y
#====================#

conn = sqlite3.connect('channels.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS channels (id INTEGER PRIMARY KEY, channel_name TEXT, invite_link TEXT)''')

conn.commit()
HEADERS = {
    'Host': 'baithek.com',
    'Content-Type': 'application/json',
    'User-Agent': 'okhttp/4.9.2'
}

user_context = {}

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @B_Y_B_Y
#====================#

def zecora_button():
    zeco = telebot.types.InlineKeyboardMarkup()
    zo1 = telebot.types.InlineKeyboardButton("🎤 تحويل إلى صوت 🎤", callback_data='tts')
    zeco.add(zo1)
    return zeco
@zo.callback_query_handler(func=lambda call: call.data == 'tts')
def text_to_speech(call):
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    text = call.message.text
    zo.answer_callback_query(callback_query_id=call.id, text="جارٍ تحويل النص إلى صوت، يرجى الانتظار...")

    try:
        lang = detect(text)
        tts = gTTS(text=text, lang=lang)
        tts.save("output.mp3")
        with open("output.mp3", 'rb') as audio:
            zo.send_voice(chat_id, audio, reply_to_message_id=message_id)
        os.remove("output.mp3")
    except Exception as e:
        zo.answer_callback_query(callback_query_id=call.id, text="حدث خطأ أثناء تحويل النص إلى صوت.")
        print(f"Error during TTS: {e}")
        
@zo.callback_query_handler(func=lambda call: call.data == 'Back')
def show_settings(call):
    markup = types.InlineKeyboardMarkup(row_width=2)

    user = zo.get_chat(call.from_user.id)
    owner_name = user.first_name
    owner_link = f"[{owner_name}](tg://user?id={call.from_user.id})"

    k_add = types.InlineKeyboardButton('➕ إضافة قناة', callback_data='add_channel')
    k_remove = types.InlineKeyboardButton('➖ حذف قناة', callback_data='remove_channel')
    k_show = types.InlineKeyboardButton('🗂 قائمة القنوات', callback_data='show_channels')
    k_delete_all = types.InlineKeyboardButton('🗑️ حذف جميع القنوات', callback_data='delete_all_channels')
    markup.add(k_show)
    markup.add(k_add, k_remove)
    markup.add(k_delete_all)
    
    zo.edit_message_text(
        chat_id=call.message.chat.id, 
        message_id=call.message.message_id,
        text=f'👤 *لوحة الأدمن*:\n\n👑 مرحباً {owner_link} في اللوحة الخاصة بك:',
        reply_markup=markup, 
        parse_mode='Markdown'
    )
    zo.clear_step_handler(call.message
    )
def subscs(user_id):
    channels = cursor.execute("SELECT channel_name, invite_link FROM channels").fetchall()  # Fetch invite link along with channel names
    for channel in channels:
        channel_username, invite_link = channel  # Unpack the invite link
        try:
            member_status = zo.get_chat_member(chat_id=channel_username, user_id=user_id).status
            if member_status not in ["member", "administrator", "creator"]:
                return False, invite_link  # Return the invite link if the user is not a member
        except Exception as e:
            continue
    return True, None

def not_subscrip(message, invite_link):  # Change parameter to invite_link
    na = message.from_user.first_name
    if invite_link:
        channel_url = invite_link.replace('@', '')
        button = telebot.types.InlineKeyboardMarkup(row_width=1)
        subscribe_button = telebot.types.InlineKeyboardButton(text="اشترك", url=f"{channel_url}")
        button.add(subscribe_button)
        zo.reply_to(
            message, 
            text=f'''
❕ | عذراً عزيزي المستخدم {na}
❗️ | يجب عليك الاشتراك في قناة المطور أولاً
❕ | اشترك ثم أرسل /start 
د==========================د
د🔗 - {invite_link}
د==========================د
''',
            disable_web_page_preview=True,
            reply_markup=button
        )
        # كلمات ثابتة وردودها
custom_replies = {
    "من صنعك": "🤖 بوت *Faresdev* صنعني، وهو شاب جزائري 🇩🇿💻",
    "من برمجك": "👨‍💻 برمجني *Faresdev*، تحية ليه ✌️",
    "من خدمك": "🔧 تم تطويري من طرف شاب جزائري مبدع 🔥",
    "من صممك": "🎨 التصميم من صنع *Faresdev* ❤️",
}
@zo.message_handler(commands=['start'])
def welcome_message(message):
    is_subscribed, channel = subscs(message.from_user.id)
    if not is_subscribed:
        not_subscrip(message, channel)
        return

    zeco = telebot.types.InlineKeyboardMarkup()
    o = telebot.types.InlineKeyboardButton("حساب المطور", url=f"https://t.me/{us}")
    c = telebot.types.InlineKeyboardButton("قناة المطور", url=f"https://t.me/{ch}")
    zeco.add(o, c)

    user_id = message.from_user.id
    first_name = message.from_user.first_name or "غير معروف"
    username = f"@{message.from_user.username}" if message.from_user.username else "غير متوفر"
    join_date = datetime.fromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S')

    user_info_text = f"""👤 معلومات المستخدم الكاملة:
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
🆔 المعرف: {user_id}
👤 الاسم: {first_name}
🔖 المعرف: {username}
📅 تاريخ الانضمام: {join_date}
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""

    welcome_text = (
        "🇩🇿 أهلا بيك خويا فـ بوت الذكاء الاصطناعي!\n"
        "🤖 نقدر نعاونك تجاوب على الأسئلة، تفهم المواضيع، ولا حتى نهدر معاك.\n\n"
        "🔰 واش تستنى؟ جرب تكتبلي أي سؤال ولا موضوع يهمك.\n\n"
        "🔒 الخدمة مجانية ومحمية.\n\n"
        "🖋️ صـنـع بـيـد: *Faresdev*"
    )

    full_text = user_info_text + "\n" + welcome_text
    zo.reply_to(message, full_text, parse_mode='Markdown', reply_markup=zeco)
@zo.message_handler(commands=['admin'])
def admin_command(message):
    user_id = message.from_user.id
    if user_id in ADMIN:
    	markup = types.InlineKeyboardMarkup(row_width=2)
    	
    	user = zo.get_chat(message.from_user.id)
    	owner_name = user.first_name
    	owner_link = f"[{owner_name}](tg://user?id={message.from_user.id})"
    	k_add = types.InlineKeyboardButton('➕ إضافة قناة', callback_data='add_channel')
    	k_remove = types.InlineKeyboardButton('➖ حذف قناة', callback_data='remove_channel')
    	k_show = types.InlineKeyboardButton('🗂 قائمة القنوات', callback_data='show_channels')
    	k_delete_all = types.InlineKeyboardButton('🗑️ حذف جميع القنوات', callback_data='delete_all_channels')
    	markup.add(k_show)
    	markup.add(k_add, k_remove)
    	markup.add(k_delete_all)
    	zo.reply_to(
                message, 
                text=f'👤 *لوحة الأدمن*:\n\n👑 مرحباً {owner_link} في اللوحة الخاصة بك:',
            reply_markup=markup, 
            parse_mode='Markdown'
        )
    else:
        zo.send_message(message.chat.id, text='🚫 عذراً، ليست لديك الصلاحية لاستخدام هذا الأمر.')
        

@zo.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    markup = types.InlineKeyboardMarkup()
    back_button = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
    markup.add(back_button)

    if call.data == 'add_channel':
        add_text = '🔹 قم بإرسال يوزر القناة بـ(@) لإضافتها :'
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=add_text, reply_markup=markup)
        zo.register_next_step_handler(call.message, add_channel)

    elif call.data == 'remove_channel':
        markup = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
        markup.add(back_button)
        delete_text = '🔸 قم بإرسال يوزر القناة بـ(@) لحذفها :'
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=delete_text,reply_markup=markup)
        zo.register_next_step_handler(call.message, remove_channel)


    elif call.data == 'delete_all_channels':
        confirmation_markup = types.InlineKeyboardMarkup()
        confirm_button = types.InlineKeyboardButton("✔️ | تأكيد الحذف | ✔️", callback_data='confirm_delete_all')
        cancel_button = types.InlineKeyboardButton("❌ | تراجع | ❌", callback_data='cancel_delete')
        confirmation_markup.add(confirm_button, cancel_button)

        confirmation_text = '''
⚠️ | *هل أنت متأكد أنك تريد حذف جميع القنوات والمجموعات؟*
✨ | *ستتم عملية الحذف بشكل نهائي*
'''
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=confirmation_text, parse_mode='Markdown', reply_markup=confirmation_markup)

    elif call.data == 'confirm_delete_all':
        cursor.execute('SELECT channel_name FROM channels')
        channels = cursor.fetchall()

        if channels:
            deletes_text = '''
👑 | عزيزي المالك 😊❤️
✔️ | *تم حذف جميع القنوات بنجاح*

🗑️ | *القنوات المحذوفة :*
د— — — — — — — — — — —
'''
            for channel in channels:
                deletes_text += f'👉 | {channel[0]}\n'
            deletes_text += 'د— — — — — — — — — — —'

            cursor.execute('DELETE FROM channels')
            conn.commit()
            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=deletes_text, parse_mode='Markdown', reply_markup=markup)

        else:
            erer_deletes_text = '''
⚠️ | عزيزي المالك 🌚❤️
❌ | *لا توجد قنوات لحذفها*
د— — — — — — — — — — —
'''
            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=erer_deletes_text, parse_mode='Markdown', reply_markup=markup)
    elif call.data == 'cancel_delete':
        cancel_text = '😮‍💨 | *تم إلغاء عملية الحذف* | 😮‍💨'
        zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=cancel_text, parse_mode='Markdown', reply_markup=markup)

    elif call.data == 'show_channels':
        cursor.execute("SELECT channel_name FROM channels")
        channels = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        if channels:
            show_text = '📋 قنوات الاشتراك الإجباري :'
            for channel in channels:
                channel_name = channel[0].replace("@", "")
                button = types.InlineKeyboardButton(
                    text=f'🔹 {channel_name}',
                    url=f'https://t.me/{channel_name}'
                )
                markup.add(button)
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            markup.add(Back)
            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=show_text, reply_markup=markup)
        else:
            not_exist_text = '❌ ¦ لا توجد قنوات مسجله حاليا ¦ ❌'
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            markup.add(Back)

            zo.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=not_exist_text, reply_markup=markup)

def add_channel(message):
    channel_name = message.text.strip()
    if not channel_name.startswith('@'):
        channel_name = '@' + channel_name
    try:
        chat_info = zo.get_chat(channel_name)
        if chat_info.type not in ['channel', 'supergroup', 'group']:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            markup.add(Back)
            text = '❌ ¦ يجب أن يكون اليوزر قناة أو مجموعة ¦ ❌'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
            return
        
        chat_members = zo.get_chat_administrators(channel_name)
        bot_is_admin = any(member.user.id == zo.get_me().id for member in chat_members)

        if not bot_is_admin:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            markup.add(Back)
            text = '🚫 ¦ يجب أن يكون البوت أدمن في القناة أو المجموعة  ¦ 🚫'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
            return

        cursor.execute("SELECT * FROM channels WHERE channel_name = ?", (channel_name,))
        channel = cursor.fetchone()

        if channel:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            Zo_text = f'''
            👑 | عزيزي المالك 😢💔
❌ | القناة موجودة بالفعل 
د— — — — — — — — — — —
د - {channel_name}
د— — — — — — — — — — —
'''
            markup.add(Back)
            zo.reply_to(message, Zo_text, reply_markup=markup)
        else:
            invite_link = zo.export_chat_invite_link(chat_info.id)
            cursor.execute("INSERT INTO channels (channel_name, invite_link) VALUES (?, ?)",
                       (channel_name, invite_link))
            conn.commit()
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            Zo_text = f'''
            👑 | عزيزي المالك 😊❤️
✔ | تم إضافة القناة بنجاح 
د— — — — — — — — — — —
د - {channel_name}
🔗 | رابط الدعوة: {invite_link}
د— — — — — — — — — — —
'''
            markup.add(Back)
            zo.reply_to(message, Zo_text, reply_markup=markup)

    except telebot.apihelper.ApiException as e:
        if "chat not found" in e.description:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            markup.add(Back)
            text = '❌ ¦ اسم القناة أو المجموعة غير صحيح ¦ ❌'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
        elif "Forbidden: bot was kicked" in e.description:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            markup.add(Back)
            text = '🚫 ¦ البوت محظور من المجموعة أو القناة ¦ 🚫'
            zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')
        else:
            zo.reply_to(message, f'خطأ: {e.description}')
    except Exception as e:
        text = f"حدث خطأ: {str(e)}"
        markup = types.InlineKeyboardMarkup()
        Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
        markup.add(Back)
        zo.reply_to(message, text=text, reply_markup=markup, parse_mode='Markdown')

def remove_channel(message):
    channel_name = message.text.strip()
    
    with sqlite3.connect('channels.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM channels WHERE channel_name = ?", (channel_name,))
        channel = cursor.fetchone()
        
        if channel:
            cursor.execute("DELETE FROM channels WHERE channel_name = ?", (channel_name,))
            conn.commit()
            
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            Zo_text = f'''
👑 | عزيزي المالك 😢💔
✔ | تم حذف القناة بنجاح 
د— — — — — — — — — — —
د - {channel_name}
د— — — — — — — — — — —
            '''
            markup.add(Back)
            zo.send_message(
                message.chat.id,
                text=Zo_text,
                reply_markup=markup
            )
        else:
            markup = types.InlineKeyboardMarkup()
            Back = types.InlineKeyboardButton("• رجوع •", callback_data='Back')
            Zo_text = f'''
👑 | عزيزي المالك 🌚❤️
❌ | القناة غير موجودة لحذفها 
د— — — — — — — — — — —
د - {channel_name}
د— — — — — — — — — — —
            '''
            markup.add(Back)
            zo.send_message(
                message.chat.id,
                text=Zo_text,
                reply_markup=markup
            )

#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @B_Y_B_Y
#====================#
@zo.message_handler(func=lambda message: True)
def handle_message(message):
    is_subscribed, channel = subscs(message.from_user.id)
    
    if not is_subscribed:
        not_subscrip(message, channel)
        return
    user_id = message.from_user.id

    user_message = message.text
    loading_message = zo.reply_to(message, "📝")
    
    if user_id not in user_context:
        user_context[user_id] = []

    user_context[user_id].append({'role': 'user', 'content': user_message})

    data = {
        'name': 'Usama',
        'messages': user_context[user_id],
        'n': 1,
        'stream': True
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        json_data = response.json()
        choices = json_data.get('choices', [])

        if choices:
            result_text = choices[0].get('message', {}).get('content', '')
            user_context[user_id].append({'role': 'assistant', 'content': result_text})

            if result_text:
                if len(result_text) > vipcode_max:
                    file_path = f'user_message_{user_id}.txt'
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(result_text)
                    with open(file_path, 'rb') as f:
                        text = '🤖 ¦ هاذا الملف يحتوي على رد البوت الطويل'
                        zo.send_document(chat_id=message.chat.id, document=f, caption=text, reply_to_message_id=message.message_id, reply_markup=zecora_button())
                    os.remove(file_path)
                else:
                    zo.edit_message_text(result_text, chat_id=message.chat.id, message_id=loading_message.message_id, reply_markup=zecora_button())
        else:
            text = '⛔️ ¦ عذراً، حاول مره اخرى لاحقاً ¦ ⛔️'
            zo.edit_message_text(text, chat_id=message.chat.id, message_id=loading_message.message_id, parse_mode='Markdown', reply_markup=zecora_button())

    except requests.RequestException as e:
        text = '⛔️ ¦ عذرًا، حدث خطأ أثناء الاتصال حاول مره اخرى لاحقاً  ¦ ⛔️'
        zo.edit_message_text(text, chat_id=message.chat.id, message_id=loading_message.message_id, parse_mode='Markdown', reply_markup=zecora_button())
        print(f"Error: {e}")
#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @B_Y_B_Y
#====================#

@zo.message_handler(func=lambda message: True)
def handle_message(message):
    is_subscribed, channel = subscs(message.from_user.id)
    if not is_subscribed:
        not_subscrip(message, channel)
        return

    if not message.text:
        return

    # ⚙️ تنظيف النص وتحضيره للمطابقة
    user_input = normalize_text(message.text)

    # ✅ ردود تلقائية مخصصة
    for key, reply_text in custom_replies.items():
        key_words = normalize_text(key).split()
        if all(word in user_input.split() for word in key_words):
            zo.send_chat_action(message.chat.id, 'typing')
            zo.reply_to(message, reply_text, parse_mode="Markdown")
            return

    # 🧠 الرد الذكي من API
    user_id = message.from_user.id
    user_message = message.text
    zo.send_chat_action(message.chat.id, 'typing')
    loading_message = zo.reply_to(message, "📝")

    if user_id not in user_context:
        user_context[user_id] = []

    user_context[user_id].append({'role': 'user', 'content': user_message})

    data = {
        'name': 'Usama',
        'messages': user_context[user_id],
        'n': 1,
        'stream': True
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        json_data = response.json()
        choices = json_data.get('choices', [])

        if choices:
            result_text = choices[0].get('message', {}).get('content', '')
            user_context[user_id].append({'role': 'assistant', 'content': result_text})

            if result_text:
                if len(result_text) > vipcode_max:
                    file_path = f'user_message_{user_id}.txt'
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(result_text)
                    with open(file_path, 'rb') as f:
                        zo.send_document(chat_id=message.chat.id, document=f, caption='🤖 ¦ هاذا الملف يحتوي على رد البوت الطويل')
                    os.remove(file_path)
                else:
                    zo.edit_message_text(result_text, chat_id=message.chat.id, message_id=loading_message.message_id)
        else:
            zo.edit_message_text('⛔️ ¦ عذراً، حاول مره اخرى لاحقاً ¦ ⛔️', chat_id=message.chat.id, message_id=loading_message.message_id)

    except requests.RequestException as e:
        zo.edit_message_text('⛔️ ¦ عذرًا، حدث خطأ أثناء الاتصال ¦ ⛔️', chat_id=message.chat.id, message_id=loading_message.message_id)
        print(f"Error: {e}")
#غير الحقوق واثبت انك فاشل اذا تريد تنقل اذكر اسمي او اسم قناتي #

#====================#
#CH : @VIPCODE3 
#DEV : @B_Y_B_Y
#====================#
import webbrowser
webbrowser.open("https://t.me/VIPCODE3")

print("🖤 لا تيأس حاول حتى يعمل 🖤")
zo.delete_webhook()
zo.infinity_polling()