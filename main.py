import asyncio
from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
# Конфигурация
BOT_TOKEN = ""
WEBHOOK_HOST = "" # Ваш домен / domain
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URI = WEBHOOK_HOST + WEBHOOK_PATH

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
from handlers import start, reviews, buy_courses, current_course, buy
from handlers.buy import payment_data

dp.include_routers(
    start.router,
    reviews.router,
    buy_courses.router,
    current_course.router,
    buy.router,
)

# FastAPI приложение
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    print("Запуск приложения...")
    await bot.set_webhook(url=WEBHOOK_URI, drop_pending_updates=True)
    print(f"Webhook установлен: {WEBHOOK_URI}")
    yield
    print("Остановка приложения...")
    await bot.delete_webhook()
    print("Webhook удалён.")

app = FastAPI(lifespan=lifespan)

@app.post("/webhook/{token}")
async def handle_webhook(request: Request, token: str):
    """Обработчик вебхука."""
    if token != BOT_TOKEN:
        print(f"Invalid token: {token}")  # Логирование некорректного токена
        raise HTTPException(status_code=400, detail="Invalid token")
    
    try:
        # Получаем данные в формате JSON
        update_data = await request.json()
        print(f"Received update data: {update_data}")  # Печать полученных данных для отладки
        
        # Преобразуем в объект Update
        telegram_update = types.Update(**update_data)
        
        # Обрабатываем обновление через feed_update
        await dp.feed_update(bot, telegram_update)  # Теперь передаем update и bot
        
        return JSONResponse(content={"status": "ok"})
    except Exception as e:
        print(f"Error: {str(e)}")  # Логирование ошибки
        raise HTTPException(status_code=500, detail="Internal Server Error")

def find_chat_by_inv_id(inv_id: int):
    for chat_id, stored_inv_id in payment_data.items():
        if stored_inv_id == inv_id:
            return chat_id
    return None

@app.post("/success/")
async def success_webhook(request: Request):
    return {"status": "success"}

@app.post("/result/")
async def result_webhook(request: Request):
    return {"status": "result"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
