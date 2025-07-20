import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode 
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- User Access Control (User Name -> User ID) ---
# Make sure you have replaced all placeholder IDs with the real ones.
user_access = {
    "Anwar": 11111111, "Alaudeen": 22222222, "Musaraf": 44444444, "Riyas": 33333333,
    "Sahul": 5337418346, "Boopathi": 6028405161, "Ijas": 1824958978, "Jaila": 1624253775
}

# --- Detailed Profile Data for Each User ---
USER_DATA = {
    "Anwar": {
        "team_id": "0101", "login": "anwar0101@gmail.com", "role": "Operation Team Leader",
        "members": ["Ajay", "Asik", "Fathah"], "groups": []
    },
    "Alaudeen": {
        "team_id": "0102", "login": "alaudeen0102@gmail.com", "role": "Operation Team Leader",
        "members": ["Mujay", "Rabik", "Faizal"], "groups": ["https://t.me/penghasiluang_online1", "https://t.me/yZnNkN"]
    },
    "Musaraf": {
        "team_id": "0103", "login": "musaraf0103@gmail.com", "role": "Operation Team Leader",
        "members": ["Mansoor", "Jassim", "Buhari"], "groups": ["https://t.me/newplatformchat", "https://t.me/epicballad_ind"]
    },
    "Riyas": {
        "team_id": "0104", "login": "riyas0104@gmail.com", "role": "Operation Team Leader",
        "members": ["Ismail", "Yousuf", "Suhair"], "groups": ["https://t.me/madmazellilekazanmayadevam", "https://t.me/Xland_com"]
    },
    "Sahul": {
        "team_id": "0105", "login": "sahul0105@gmail.com", "role": "Operation Team Leader",
        "members": ["Sameen", "Ajay_2", "Rahman"], "groups": ["https://t.me/+xfQQT3ZHzfNkM2Q6", "https://t.me/ALKEN_LUX_INVISTETSION_GROUP"]
    },
    "Boopathi": {
        "team_id": "0100", "login": "boopathi100@gmail.com", "role": "Project Manager",
        "members": ["Musaraf", "Sahul"], "groups": ["https://t.me/epic_balled_india", "https://t.me/RoyalWinOfficialGroup888", "https://t.me/merobit_net"]
    },
    "Ijas": {
        "team_id": "0100", "login": "ijas100@gmail.com", "role": "Project Manager",
        "members": ["Anwar", "Alaudeen", "Riyas"], "groups": ["https://t.me/epic_balled_india", "https://t.me/RoyalWinOfficialGroup888", "https://t.me/merobit_net"]
    },
    "Jaila": {
        "team_id": "0106", "login": "jaila0106@gmail.com", "role": "Operation Team Leader",
        "members": ["Team Member 1", "Team Member 2"], "groups": []
    }
}

# --- Bot Command and Message Handlers ---

# MODIFIED: This function now adds emojis to user names and includes the "Login Now" button
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends the main menu using ReplyKeyboardMarkup."""
    user_buttons = list(USER_DATA.keys())
    keyboard_layout = []
    for i in range(0, len(user_buttons), 2):
        # NEW: Add emoji before each user name
        row = [KeyboardButton(f"🧑‍💻 {user_buttons[i]}")]
        if i + 1 < len(user_buttons):
            row.append(KeyboardButton(f"🧑‍💻 {user_buttons[i+1]}"))
        keyboard_layout.append(row)

    # NEW: Add "Login Now" button at the bottom of the keyboard
    keyboard_layout.append([KeyboardButton("✅ Login Now")])

    reply_markup = ReplyKeyboardMarkup(
        keyboard_layout, 
        resize_keyboard=True, 
        one_time_keyboard=True
    )
    
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
    
    await context.bot.send_message(
        chat_id=chat_id,
        text="Please select your name from the keyboard below 👇",
        reply_markup=reply_markup
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    await send_main_menu(update, context)

# MODIFIED: Handles new "Login Now" button and user names with emojis
async def handle_user_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles when a user presses a button on the reply keyboard."""
    user_input_text = update.message.text
    user_id = update.message.from_user.id

    # NEW: Handle the "Login Now" button press
    if user_input_text == "✅ Login Now":
        login_url = "https://jaila202.github.io/my-ciphercoin-report/"
        inline_keyboard = [[InlineKeyboardButton("Click Here to Open Login Page", url=login_url)]]
        inline_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(
            "Click the button below to log in.",
            reply_markup=inline_markup
        )
        return

    # NEW: Clean the emoji from the user name before checking it
    cleaned_name = user_input_text.lstrip("🧑‍💻 ")

    if cleaned_name in USER_DATA:
        if user_id == user_access.get(cleaned_name):
            data = USER_DATA[cleaned_name]
            team_members_str = "\n".join([f"              {i+1}. {name}" for i, name in enumerate(data['members'])])
            
            if data['groups']:
                assignment_groups_str = "\n".join([f"👉 [Group Link {i+1}]({link})" for i, link in enumerate(data['groups'])])
            else:
                assignment_groups_str = "No groups assigned."

            # Use the original text with emoji for the name field
            reply_text = (
                f"*Name* : {user_input_text}\n"
                f"*Team ID* : {data['team_id']}\n\n"
                f"*User Login* : `{data['login']}`\n"
                f"*Password* : `123456`\n"
                f"*Role* : {data['role']}\n"
                f"*Team Members* : \n{team_members_str}\n\n"
                f"*Assignment Groups* : \n{assignment_groups_str}"
            )
            
            login_url = "https://jaila202.github.io/my-ciphercoin-report/"
            profile_keyboard = [
                [InlineKeyboardButton("✅ Login Now", url=login_url)],
                [InlineKeyboardButton("⬅️ Back to Menu", callback_data="show_main_menu")]
            ]
            inline_markup = InlineKeyboardMarkup(profile_keyboard)

            await update.message.reply_text(
                reply_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=inline_markup,
                disable_web_page_preview=True
            )
        else:
            await update.message.reply_text(
                "❌ *Access Denied*. This profile is not for you.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ReplyKeyboardRemove()
            )

async def inline_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles callback queries from the 'Back to Menu' inline button."""
    query = update.callback_query
    await query.answer()

    if query.data == "show_main_menu":
        await query.message.delete()
        await send_main_menu(update, context)

# --- Main Bot Setup ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found. Please add it to your Replit Secrets.")

app = ApplicationBuilder().token(TOKEN).build()

# Register the handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(inline_button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_selection))

print("Bot is running...")
app.run_polling()
