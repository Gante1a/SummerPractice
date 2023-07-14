import json
from database import DatabaseManager, UserMain, UserOptional, UserKeys
import httpx
import asyncio

class UserSaver:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        self.bot_token = config_data['bot_token']
        self.url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.database = DatabaseManager(config_file=config_file)

    async def handle_message(self, update):
        # Данные для таблицы
        message = update['message']
        chat_id = message['from']['id']
        first_name = message['from']['first_name']
        username = message['from'].get('username')
        user = self.database.session.query(UserMain).filter_by(chat_id=chat_id).first()

        if user is None:
            await self.save_user_data(chat_id, first_name, username)
            await self.reply_text(chat_id, "Спасибо, ваши данные сохранены!")
        else:
            await self.reply_text(chat_id, "Ваши данные уже сохранены в базе данных!")

        # Проверка наличия текста сообщения
        if 'text' in message:
            message_text = message['text']
            key = self.database.session.query(UserKeys).filter_by(key=message_text).first()

            if key:
                # Добавление имени при вводе определённого значения
                user_optional = self.database.session.query(UserOptional).filter_by(chat_id=chat_id).first()

                if user_optional:
                    user_optional.official_name = key.official_name
                    self.database.session.commit()
                    await self.reply_text(chat_id, f"Ваше имя обновлено на: {key.official_name}")

                # Удаление ключа из таблицы
                self.database.session.delete(key)
                self.database.session.commit()

    async def save_user_data(self, chat_id, first_name, username):
        # Сохранение данных в таблицы users_main и users_optional
        user_main = UserMain(chat_id=chat_id, first_name=first_name, username=username)
        user_optional = UserOptional(chat_id=chat_id, official_name='', group='')
        self.database.session.add(user_main)
        self.database.session.add(user_optional)
        self.database.session.commit()

    async def reply_text(self, chat_id, text):
        # Отправка сообщения пользователю
        reply_url = f"{self.url}sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(reply_url, json=payload)
            if response.status_code != 200:
                print('Ошибка при отправке сообщения')

    async def start(self):
        offset = None
        while True:
            try:
                updates_url = f"{self.url}getUpdates?offset={offset}"
                response = httpx.get(updates_url)
                json_response = response.json()
                if response.status_code == 200 and json_response['ok']:
                    updates = json_response['result']
                    if updates:
                        for update in updates:
                            await self.handle_message(update)
                            offset = update['update_id'] + 1
            except httpx.RequestError:
                print("Ошибка при подключении к интернету. Ожидание подключения...")
                await asyncio.sleep(5)

def run_user_saver():
    user_saver = UserSaver()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(user_saver.start())

if __name__ == "__main__":
    run_user_saver()
