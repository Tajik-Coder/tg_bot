# Telegram AI Bot

Телеграм бот на Python с использованием ИИ (например, GPT), который может отвечать на сообщения пользователей в реальном времени.

## Функционал
- Общение с пользователем через Telegram
- Подключение к модели ИИ для генерации ответов
- Поддержка текстовых и мультимедийных сообщений
- Логирование чата в базу данных (опционально)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Tajik_Coder/telegram-ai-bot.git
cd telegram-ai-bot
```
2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
3. Создайте файл api_token.py с вашим токеном Telegram бота:
```bash
TOKEN = "ВАШ_ТОКЕН_ТЕЛЕГРАМ"
```
4. Запустите бота:
```bash
python bot.py
```
5. Структура проекта:
```bash
telegram-ai-bot/
│
├─ bot.py                # Основной файл бота
├─ api_token.py          # Файл с токеном
├─ requirements.txt      # Зависимости
├─ chat_history.db       # Опциональная база данных
└─ README.md             # Этот файл
```
