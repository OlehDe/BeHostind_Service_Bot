from dotenv import load_dotenv
import os

load_dotenv()  # читає .env з тієї ж папки

# Тут ми беремо значення з файлу .env по імені змінної
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
