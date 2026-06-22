from config import bot

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(
        message, 
        f"Hello {message.from_user.first_name}! I am online and running without an API ID."
    )
