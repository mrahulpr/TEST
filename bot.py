import logging
import math
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your actual Telegram Bot Token
BOT_TOKEN = "8532515086:AAEv3PznfTARrV6VFZISRExKOfFYdQcOGMI"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def get_keyboard(display: str) -> InlineKeyboardMarkup:
    """Generates the calculator keyboard layout."""
    # Ensure display fits or shows default
    disp_text = display if display else "0"
    
    keyboard = [
        # Display Row (Clicking it does nothing)
        [InlineKeyboardButton(text=disp_text, callback_data="IGNORE")],
        # Row 1
        [
            InlineKeyboardButton(text="%", callback_data="OP_%"),
            InlineKeyboardButton(text="CE", callback_data="CLR_CE"),
            InlineKeyboardButton(text="C", callback_data="CLR_C"),
            InlineKeyboardButton(text="⌫", callback_data="CLR_BACK")
        ],
        # Row 2
        [
            InlineKeyboardButton(text="¹/x", callback_data="FUNC_INV"),
            InlineKeyboardButton(text="x²", callback_data="FUNC_SQ"),
            InlineKeyboardButton(text="²√x", callback_data="FUNC_SQRT"),
            InlineKeyboardButton(text="÷", callback_data="OP_/")
        ],
        # Row 3
        [
            InlineKeyboardButton(text="7", callback_data="NUM_7"),
            InlineKeyboardButton(text="8", callback_data="NUM_8"),
            InlineKeyboardButton(text="9", callback_data="NUM_9"),
            InlineKeyboardButton(text="×", callback_data="OP_*")
        ],
        # Row 4
        [
            InlineKeyboardButton(text="4", callback_data="NUM_4"),
            InlineKeyboardButton(text="5", callback_data="NUM_5"),
            InlineKeyboardButton(text="6", callback_data="NUM_6"),
            InlineKeyboardButton(text="—", callback_data="OP_-")
        ],
        # Row 5
        [
            InlineKeyboardButton(text="1", callback_data="NUM_1"),
            InlineKeyboardButton(text="2", callback_data="NUM_2"),
            InlineKeyboardButton(text="3", callback_data="NUM_3"),
            InlineKeyboardButton(text="+", callback_data="OP_+")
        ],
        # Row 6
        [
            InlineKeyboardButton(text="+/—", callback_data="FUNC_SIGN"),
            InlineKeyboardButton(text="0", callback_data="NUM_0"),
            InlineKeyboardButton(text=".", callback_data="NUM_."),
            InlineKeyboardButton(text="=", callback_data="EQUAL")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the calculator interface."""
    context.user_data["expr"] = ""  # Stores current math expression
    await update.message.reply_text("Calculator:", reply_markup=get_keyboard("0"))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button interactions."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data == "IGNORE":
        return

    # Initialize session data if missing
    if "expr" not in context.user_data:
        context.user_data["expr"] = ""
        
    expr = str(context.user_data["expr"])

    # Handle Numbers & Decimals
    if data.startswith("NUM_"):
        val = data.split("_")[1]
        expr += val

    # Handle Standard Operators
    elif data.startswith("OP_"):
        op = data.split("_")[1]
        if expr and expr[-1] not in "+-*/%":
            expr += op

    # Handle Clears
    elif data == "CLR_C" or data == "CLR_CE":
        expr = ""
    elif data == "CLR_BACK":
        expr = expr[:-1]

    # Handle Special Functions
    elif data.startswith("FUNC_"):
        func = data.split("_")[1]
        try:
            # We evaluate the current string to apply the single-variable function
            current_val = float(eval(expr)) if expr else 0.0
            if func == "INV":
                expr = str(1 / current_val)
            elif func == "SQ":
                expr = str(current_val ** 2)
            elif func == "SQRT":
                expr = str(math.sqrt(current_val))
            elif func == "SIGN":
                expr = str(-current_val)
        except Exception:
            expr = "Error"

    # Handle Evaluation
    elif data == "EQUAL":
        try:
            # Dangerous in production web apps, but fine for simple bot calculator logic
            if expr:
                # Basic sanitation for percentage
                sanitized = expr.replace("%", "/100")
                result = eval(sanitized)
                # Format to strip trailing zeros if integer
                expr = f"{result:g}" if isinstance(result, (int, float)) else str(result)
        except Exception:
            expr = "Error"

    # Update state and UI
    context.user_data["expr"] = expr
    display_text = expr if expr not in ("", "Error") else (expr if expr == "Error" else "0")
    
    try:
        await query.edit_message_text("Calculator:", reply_markup=get_keyboard(display_text))
    except Exception:
        # Prevents crash if message text didn't change
        pass

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
