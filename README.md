## Запуск бота (через Docker)

1. **Склонируй репозиторий:**
```bash
git clone https://github.com/Espristars/AIBot.git
cd AIBot
```
2. **Создайте файл .env:**
```bash
BOT_TOKEN=telegram_bot_token
OPENAI_API_KEY=openai_api_key
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/dbname
```
3. **Разверните Docker-compose:**
```bash
docker-compose up --build
```