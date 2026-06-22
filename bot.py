import os
import importlib
from config import bot

def load_plugins():
    # Scan the plugins folder and import every python file
    for file in os.listdir("plugins"):
        if file.endswith(".py") and not file.startswith("__"):
            importlib.import_module(f"plugins.{file[:-3]}")

if __name__ == "__main__":
    load_plugins()
    print("Bot is online!")
    bot.infinity_polling()
