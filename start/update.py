import os
import sys
import subprocess
from config import bot, OWNER_ID

@bot.message_handler(commands=['update'])
def update_cmd(message):
    # Security check: only allow the owner
    if message.from_user.id != OWNER_ID:
        return

    msg = bot.reply_to(message, "Checking GitHub for updates...")
    
    # Execute git pull command
    result = subprocess.run(["git", "pull"], capture_output=True, text=True)
    
    if "Already up to date." in result.stdout:
        bot.edit_message_text("The code is already up to date.", chat_id=msg.chat.id, message_id=msg.message_id)
        return

    bot.edit_message_text("Updates pulled. Restarting the system...", chat_id=msg.chat.id, message_id=msg.message_id)
    
    # Restart the script
    os.execl(sys.executable, sys.executable, "bot.py")
