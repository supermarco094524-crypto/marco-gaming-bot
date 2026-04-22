import telebot
import requests

# Bot Configuration
API_TOKEN = '8725726743:AAFZlnmhMbBi_LGvvGNsquQ-h8qvsM4sEfQ'
ADMIN_ID = 7617135270
API_URL = "https://sacoliofficial.com/api/api/games/check_region"

bot = telebot.TeleBot(API_TOKEN)

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 မင်္ဂလာပါ Marco Gaming Shop မှ ကြိုဆိုပါတယ်။\n\nMLBB ID စစ်ဆေးရန် `/check GameID ZoneID` ဟု ရိုက်နှိပ်ပါ။")

@bot.message_handler(commands=['check'])
def check_ml_id(message):
    # Admin ဟုတ်မဟုတ် စစ်ဆေးခြင်း
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ စိတ်မရှိပါနဲ့။ ဒီ Command ကို Admin သာ အသုံးပြုခွင့်ရှိပါတယ်။")
        return

    # User ရိုက်လိုက်တဲ့ command ကို ခွဲထုတ်ခြင်း (e.g. /check 1012720981 13056)
    msg_parts = message.text.split()
    
    if len(msg_parts) < 3:
        bot.reply_to(message, "⚠️ အသုံးပြုပုံ မှားယွင်းနေပါတယ်။\nFormat: `/check GameID ZoneID` ဟုရိုက်ပါ။", parse_mode="Markdown")
        return

    game_id = msg_parts[1]
    zone_id = msg_parts[2]

    # Loading message
    status_msg = bot.reply_to(message, "⏳ ခေတ္တစောင့်ဆိုင်းပေးပါ...")

    try:
        # API သို့ Data ပေးပို့ခြင်း
        payload = {
            'game_id': game_id,
            'zone_id': zone_id
        }
        response = requests.post(API_URL, data=payload)
        data = response.json()

        if response.status_code == 200 and data.get('status') == 'success':
            # အကောင့်နာမည်ကို copy ကူးရလွယ်အောင် `code` format ဖြင့်ပြခြင်း
            nickname = data.get('nickname', 'Not Found')
            region = data.get('region', 'Unknown')

            reply_text = (
                f"🎮 *Marco Gaming Shop*\n"
                f"━━━━━━━━━━━━━━━\n"
                f"✅ *Account Verified*\n\n"
                f"👤 Name: `{nickname}`\n"
                f"🌎 Region: {region}\n"
                f"🆔 ID: {game_id} ({zone_id})\n\n"
                f"📌 *Copy ကူးရန် Name အပေါ်သို့ နှိပ်ပါ။*"
            )
            bot.edit_message_text(reply_text, message.chat.id, status_msg.message_id, parse_mode="Markdown")
        else:
            bot.edit_message_text("❌ အချက်အလက် ရှာမတွေ့ပါ။ ID နှင့် Zone မှန်ကန်မှု ရှိမရှိ ပြန်စစ်ပေးပါ။", message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❗ Error ဖြစ်ပွားခဲ့သည်: {str(e)}", message.chat.id, status_msg.message_id)

# Bot ကို စတင်ခြင်း
print("Bot is running...")
bot.infinity_polling()
