import telebot
import requests

# Bot Configuration
API_TOKEN = '8725726743:AAFZlnmhMbBi_LGvvGNsquQ-h8qvsM4sEfQ'
ADMIN_ID = 7617135270

bot = telebot.TeleBot(API_TOKEN)

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🎮 *Marco Gaming Shop မှ ကြိုဆိုပါတယ်*\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "MLBB Account Name စစ်ဆေးရန် အောက်ပါအတိုင်း ရိုက်ပါ -\n\n"
        "👉 `/check GameID ZoneID`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['check'])
def check_id(message):
    # Admin Check
    if not is_admin(message.from_user.id):
        bot.reply_to(message, "❌ ဒီ Bot ကို Admin သာ အသုံးပြုခွင့်ရှိပါတယ်။")
        return

    msg_parts = message.text.split()
    if len(msg_parts) < 3:
        bot.reply_to(message, "⚠️ Format မှားနေပါတယ်။\nဥပမာ - `/check 1012720981 13056`", parse_mode="Markdown")
        return

    game_id = msg_parts[1]
    zone_id = msg_parts[2]
    status_msg = bot.reply_to(message, "🔍 အချက်အလက် ရှာဖွေနေပါသည်...")

    try:
        # Public API Endpoint (isan.eu.org)
        api_url = f"https://api.isan.eu.org/nickname/ml?id={game_id}&zone={zone_id}"
        
        response = requests.get(api_url, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # API response က "name" key နဲ့ ပြန်ပေးပါတယ်
            name = data.get('name')

            if name:
                result_text = (
                    f"🎮 *Marco Gaming Shop*\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"✅ *Account Verified*\n\n"
                    f"👤 Name: `{name}`\n"
                    f"🆔 ID: {game_id} ({zone_id})\n\n"
                    f"📌 *နာမည်ကို နှိပ်၍ Copy ယူနိုင်ပါသည်။*"
                )
                bot.edit_message_text(result_text, message.chat.id, status_msg.message_id, parse_mode="Markdown")
            else:
                bot.edit_message_text("❌ အချက်အလက် ရှာမတွေ့ပါ။ ID နှင့် Zone ပြန်စစ်ပေးပါ။", message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text(f"❌ API Error: {response.status_code} ဖြစ်နေပါသည်။", message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❗ ချိတ်ဆက်မှု အဆင်မပြေပါ- {str(e)}", message.chat.id, status_msg.message_id)

# Start Bot
print("Bot is running...")
bot.infinity_polling()

