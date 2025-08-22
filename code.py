import sqlite3
import random
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import nest_asyncio

# Применяем patch для работы в Jupyter
nest_asyncio.apply()

# Токен бота
TELEGRAM_TOKEN = '7957614897:AAF5jntIq8mm_97_rVdZpTYY8bc8OrD3Prg'

# Инициализация базы данных
def init_db():
    # Удаляем старую базу, если она есть
    if os.path.exists('memes1.db'):
        os.remove('memes1.db')
    
    conn = sqlite3.connect('memes1.db')
    c = conn.cursor()
    
    # Создаем таблицу с правильной структурой
    c.execute('''CREATE TABLE memes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 url TEXT NOT NULL,
                 theme TEXT NOT NULL)''')
    
    # Добавляем тестовые мемы
    test_memes = [
        ('https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif', 'котики'),
        ('https://media.giphy.com/media/Kc3FsPX7MWtsQ/giphy.gif', 'котики'),
        ('https://i.pinimg.com/736x/e3/30/84/e33084a681a25e8df8c2aecf88078b04.jpg', 'котики'),
        ('https://i.pinimg.com/736x/42/f0/13/42f0137a82206abb3d758a518c9a4b30.jpg', 'котики'),
        ('https://i.pinimg.com/736x/32/85/de/3285de3c0f80eb856f1274f9d9397303.jpg', 'котики'),
        ('https://i.pinimg.com/736x/4f/e2/a9/4fe2a99719a57a447f5932e166a4372f.jpg', 'котики'),
        ('https://i.pinimg.com/736x/82/ff/5f/82ff5fffb46fba46acafc100d78aea7c.jpg', 'котики'),
        ('https://i.pinimg.com/736x/6f/0c/7d/6f0c7dd236a49fef3d2c7ad9def7f87c.jpg', 'котики'),
        ('https://media.giphy.com/media/e8bzp1IEORteM/giphy.gif', 'котики'),
        ('https://media.giphy.com/media/xj3Ie4rLNuLSM/giphy.gif', 'котики'),
        ('https://media.giphy.com/media/3o8dp5JJxpApGJE5m8/giphy.gif', 'котики'),
        ('https://media.giphy.com/media/9IRX12VhoXoR2/giphy.gif', 'котики'),
        ('https://i.pinimg.com/736x/b8/46/7a/b8467a03c6cf99bd9cee44b33c2d35ca.jpg', 'котики'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2ZnYmdpdnFmaGtna3M1ZWZycnYzbWFuZHNqc2g4dzhqMG50YjBybSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/q1MeAPDDMb43K/giphy.gif', 'котики'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExajFpN3JmMGFvYWJjZW93MWl1MnpmdjhwZHM5YjQ0ZjVoazVydXpldSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/aTUrF9TPZYy6Q/giphy.gif', 'котики'),
        ('https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExd3BuMDNhZThhMGxvYXQ1aG51dW94aHdycXNvc3U4ZWd0NjZiazJydCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wr7oA0rSjnWuiLJOY5/giphy.gif','котики'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdW1zazhlMmR0NDVoMjBzdHQyNnJjYjV6OGhtMXM4cnY4Mmk0NW9xMiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/GeimqsH0TLDt4tScGw/giphy.gif', 'котики'),
        ('https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWJhZmt4YnhrdzJiZ21kYWs5NnQ3azI4OHllcXZiMHY0czduc2xlNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/24MuxVfDmcDAIynwPx/giphy.gif', 'котики'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHo4ZDk3d3BncGszZHIxNWh6aHgxZG43a2U3cDJubnhjNjVydXY5OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Wwn5NKv4At2CIc8XQa/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHo4ZDk3d3BncGszZHIxNWh6aHgxZG43a2U3cDJubnhjNjVydXY5OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Z5xk7fGO5FjjTElnpT/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHo4ZDk3d3BncGszZHIxNWh6aHgxZG43a2U3cDJubnhjNjVydXY5OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/x9rcOPNqshtxlz9kSE/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHo4ZDk3d3BncGszZHIxNWh6aHgxZG43a2U3cDJubnhjNjVydXY5OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3otPouK6uFVTilK6xa/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHo4ZDk3d3BncGszZHIxNWh6aHgxZG43a2U3cDJubnhjNjVydXY5OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/ukwPlCmJ5RmlqvQCpA/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHo4ZDk3d3BncGszZHIxNWh6aHgxZG43a2U3cDJubnhjNjVydXY5OSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/qx9p83pYWelxxqDAsB/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif', 'собаки'),
        ('https://media.giphy.com/media/35DmVHlLURCWBxmK8j/giphy.gif', 'собаки'),
        ('https://i.imgur.com/7G9fH.jpg', 'собаки'),
        ('https://i.pinimg.com/736x/88/6c/58/886c589bab3d659d8cedc5702e816da3.jpg', 'собаки'),
        ('https://i.pinimg.com/736x/07/0f/fc/070ffcbf68d110520f97e0e5503fcc8a.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/19/a7/fa/19a7fa4f84b1a9b0528ca1ae3f85e9af.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/3f/bf/cf/3fbfcfae3b0baf831ddc9676813e965b.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/cd/a0/dd/cda0ddb46f7b699af4ddae32565caf1e.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/e6/23/43/e623430bfb7f06054e498a39f905e25a.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/be/69/17/be6917f60214cf1b77dcba4f68a0b9fe.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/4b/9f/84/4b9f84ab7e4546e94699588885beac55.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/8c/88/87/8c8887290d3f82402764e9e5e3edf53a.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/5f/61/43/5f6143e76019c3fb219d7eb5f337acc4.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/ce/14/cc/ce14cccd9c424f14a909552f63641d2c.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/53/5b/4c/535b4ce7351b07c3ed8a79b4944ef436.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/41/4d/6b/414d6b4bcdceff9366cdb78fa17fef35.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/11/a7/94/11a794c2280eab49b2bd639027b20f2e.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/bc/16/9d/bc169d4d4c649b95988db095b84c4084.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/f7/a7/30/f7a73039cf3f1ce91a2461052e62115f.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/19/a7/fa/19a7fa4f84b1a9b0528ca1ae3f85e9af.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/f1/99/03/f19903197b383ab141741f83d1991d02.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/b6/ba/a6/b6baa6dac24a45f662481ed18923b457.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/26/29/cc/2629cc22ca2e2f640e93cf417140ba67.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/72/9f/3c/729f3cc83c9ddbf3be384532f90ac93b.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/fe/f7/8e/fef78e8ef4aad41623526ee97023a6d3.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/f2/b6/be/f2b6be706f611a931fb089bbfa4546bd.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/32/c8/aa/32c8aaad456571ed7714d91c5884aeea.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/32/c8/aa/32c8aaad456571ed7714d91c5884aeea.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/ec/d6/1e/ecd61ea8fbcca23b3672930e4ca93cdd.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/5c/0b/6c/5c0b6cb34a93a60d90cbc66b41a37c98.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/98/36/3f/98363feacbf22abe1e3a7b1cd3262e5a.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/9b/d2/0d/9bd20d554d38da049c6eaa447316d1d3.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/c7/dc/58/c7dc58229ec526d73028247a311ffba7.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/b5/57/cc/b557ccbcffd22f9069b03d1b47408f94.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/80/ab/3f/80ab3fb70f9de53c8f892eafe726b686.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/9b/14/94/9b1494a48c1e0d8df0886ad879f769de.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/31/bc/91/31bc91ecfe332d4919d2277f686e5c5a.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/75/91/00/759100161a1056e5c890cf3d767ce8c4.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/af/b4/20/afb420d7596623732c2bde303c34d16b.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/bd/9a/e1/bd9ae1948ab519dcc873554d23b791d7.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/f3/64/76/f364765db4a3f90db2bd9c3073e7451c.jpg', 'юмор'),
        ('https://i.pinimg.com/736x/8a/28/4d/8a284d736fb6df8705f545284c76febf.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/c5/57/40/c5574025107cc1fe17844db4d8087331.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/e9/f7/d9/e9f7d9d6cdd3a6ffec107828533af39c.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/c9/00/77/c90077a8468e937e0f9fb7c84d9d6589.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/15/0b/9f/150b9fcaf6a277bae1fc2b740f886f94.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/e4/df/cd/e4dfcd497e6c1a366f185dba58a10072.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/74/95/90/749590568ef8f5cd7a68fef7d71589c4.jpg', 'итальянсике животные'),
        ('https://i.pinimg.com/736x/54/cd/99/54cd9941fe3ddd897cba0b3087de0473.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/ae/f3/e6/aef3e6603ee2f500af13cfa5d882f59a.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/8c/21/1a/8c211af6ac348ccd5e8ff88e1b85df07.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/45/08/3b/45083b129b9bd3d05ef7c0a5879035db.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/27/fa/d6/27fad694eb74d105cb2828e84611e69c.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/8e/6c/42/8e6c4299b15f7acda75d1275eda35a5a.jpg', 'итальянские животные'),
        ('https://i.pinimg.com/736x/88/6c/58/886c589bab3d659d8cedc5702e816da3.jpg', 'собаки'),
        ('https://media.giphy.com/media/1qB3EwE3c54A/giphy.gif','черепашки'),
        ('https://i.pinimg.com/736x/12/9c/dc/129cdc63706429f9473142ad77dc1ec9.jpg', 'черепашки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXR2ajVsdnQxbTRpeTE3NGJsNGtqazR1dG53cHdhcWIyb2k2MTZyNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/gYbSF7RP9eUzC/giphy.gif', 'черепашки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXR2ajVsdnQxbTRpeTE3NGJsNGtqazR1dG53cHdhcWIyb2k2MTZyNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kKzFYlqCv7yDe/giphy.gif', 'черепашки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXR2ajVsdnQxbTRpeTE3NGJsNGtqazR1dG53cHdhcWIyb2k2MTZyNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/cFdHXXm5GhJsc/giphy.gif', 'черепашки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExeXR2ajVsdnQxbTRpeTE3NGJsNGtqazR1dG53cHdhcWIyb2k2MTZyNCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/jPMVgIAzYEruM/giphy.gif', 'черепашки'),
        ('https://media.giphy.com/media/vzOhKYvn96uhG/giphy.gif', 'черепашки'),
        ('https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExc3dlNjNxMWc0bHg0cG1oaWxpczhyMnNhc210dDJnNnBqYXptaGZnbSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/uA8WItRYSRkfm/giphy.gif', 'краб'),
        ('https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWU4c3QyNXpmcjFzN2Z2dDk0aHBvbjV3Z2xmamtlNXl3cXdxdzI0biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/gktOiCyL1zdde/giphy.gif', 'краб'),
        ('https://media.giphy.com/media/3oGRFH0T7pIEpYdTNe/giphy.gif', 'краб'),
        ('https://media.giphy.com/media/2OH3bMizhs8aA/giphy.gif', 'краб'),
        ('https://media.giphy.com/media/3ohuPtorn7OmTiq0ta/giphy.gif', 'краб'),
        ('https://i.pinimg.com/736x/28/7d/a0/287da088bbb2740fb39a44b5bc740f6f.jpg', 'курица'),
        ('https://i.pinimg.com/736x/72/ed/0a/72ed0ad22e9846e875c285363468d6e7.jpg', 'курица'),
        
    ]
    c.executemany('INSERT INTO memes (url, theme) VALUES (?, ?)', test_memes)
    conn.commit()
    conn.close()
    print("База данных 'memes1.db' создана и заполнена тестовыми мемами!")

# Функция для получения случайного мема
def get_meme(theme=None):
    conn = sqlite3.connect('memes1.db')
    c = conn.cursor()
    
    if theme:
        c.execute('SELECT url FROM memes WHERE theme LIKE ?', (f'%{theme.lower()}%',))
    else:
        c.execute('SELECT url FROM memes')
    
    memes = c.fetchall()
    conn.close()
    
    return random.choice(memes)[0] if memes else None

# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Привет! Я бот для поиска мемов.\n'
        'Используй команды:\n'
        '/meme - случайный мем\n'
        '/meme тема - мем по теме (Пример: /meme котики)\n'
        'Возможные темы для поиска - юмор, котики, собаки,черепашки,итальянские животные, краб, курица'
    )

async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    theme = ' '.join(context.args) if context.args else None
    meme_url = get_meme(theme)
    
    if meme_url:
        try:
            if meme_url.endswith('.gif'):
                await update.message.reply_animation(meme_url)
            else:
                await update.message.reply_photo(meme_url)
        except Exception as e:
            await update.message.reply_text(f'Ошибка при отправке мема: {e}')
    else:
        await update.message.reply_text('Мемы по этой теме не найдены 😢 Попробуй другую тему!')

# Запуск бота
def run_bot():
    # Инициализируем базу данных
    init_db()
    
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('meme', meme))
    
    # Запускаем бота
    print("Бот запущен! Перейдите в Telegram и начните общение с ботом.")
    print("Для остановки бота перезапустите ядро Jupyter.")
    application.run_polling()

# Запускаем бота
run_bot()
