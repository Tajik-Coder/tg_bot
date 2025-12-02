import sqlite3
from io import BytesIO
from PIL import Image
import pytesseract
import g4f
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio
from api_token import TOKEN
# ====== TOKEN ======


# ====== Database setup ======
DB_FILE = "chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        role TEXT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_message(user_id, role, content):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)",
                   (user_id, role, content))
    conn.commit()
    conn.close()

def load_history(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM history WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in rows]

# ====== Bot setup ======
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ====== /start ======
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(f"Салом, Абдуллохон! Ман боти шахсии Шумо ҳастам. Ба ман чи саволе дошта бошед аз ман пурсед!")

# ====== Матн ======
@dp.message(lambda msg: msg.content_type == "text")
async def gpt_response(message: Message):
    user_id = str(message.from_user.id)
    user_text = message.text

    # Бор кардани таърихи пешин
    history = load_history(user_id)
    history.append({"role": "user", "content": user_text})
    save_message(user_id, "user", user_text)

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=history
        )
        save_message(user_id, "assistant", response)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Хато шуд: {e}")

# ====== Расм ======
@dp.message(lambda msg: msg.content_type == "photo")
async def image_response(message: Message):
    user_id = str(message.from_user.id)

    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    file_bytes = await bot.download_file(file.file_path)

    image = Image.open(BytesIO(file_bytes.getvalue()))
    text_from_image = pytesseract.image_to_string(image, lang="eng")

    if not text_from_image.strip():
        text_from_image = "[Дар расм матн ёфта нашуд]"

    # Бор кардани таърихи пешин
    history = load_history(user_id)
    history.append({"role": "user", "content": f"Image text: {text_from_image}"})
    save_message(user_id, "user", f"Image text: {text_from_image}")

    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4",
            messages=history
        )
        save_message(user_id, "assistant", response)
        await message.answer(response)
    except Exception as e:
        await message.answer(f"Хато шуд: {e}")

# ====== Start bot ======
async def main():
    init_db()
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
