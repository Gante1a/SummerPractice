import json
from jinja2 import Template
from datetime import datetime
from database import DatabaseManager, UserMain, UserMessages
import time
import httpx

class MessageSender:
    def __init__(self, chat_id, message, config_file='config.json'):
        self.chat_id = chat_id
        self.message = message

        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        self.bot_token = config_data['bot_token']
        self.template = Template(config_data['template_message'])
        self.database = DatabaseManager(config_file=config_file)

    async def send_message(self):
        # Запрос chat_id по chat_id
        user = self.database.session.query(UserMain).filter_by(chat_id=self.chat_id).first()
        if user is None:
            print('Введённые данные некорректные, повторите ввод')
            return

        # Применение jinja
        message_text = self.template.render(message=self.message)
        # Запись сообщения в базу данных со статусом is_sent = 0 (не отправлено)
        telegram_server_time = datetime.now()
        telegram_server_time_str = telegram_server_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        new_message = UserMessages(chat_id=user.chat_id, message=message_text, time=telegram_server_time_str, is_sent=False)
        self.database.session.add(new_message)
        self.database.session.commit()

        while True:
            if await self.check_internet_connection():
                # Обновление статуса сообщения в базе данных на 1 (отправлено)
                new_message.is_sent = True
                self.database.session.commit()
                # Отправка сообщения
                send_message_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                payload = {
                    'chat_id': user.chat_id,
                    'text': message_text
                }
                async with httpx.AsyncClient() as client:
                    response = await client.post(send_message_url, json=payload)
                    if response.status_code == 200:
                        print('Сообщение было успешно отправлено пользователю')
                    else:
                        print('Ошибка при отправке сообщения')
                break
            else:
                # Проверка подключения к интернету каждые 5 секунд
                print('Сообщение не было отправлено, проверьте подключение к интернету')
                print('Ожидание подключения к интернету...')
                time.sleep(5)

        self.database.close()

    async def check_internet_connection(self):
        try:
            # Проверка подключения к интернету
            async with httpx.AsyncClient() as client:
                response = await client.get("https://web.telegram.org")
                return response.status_code == 200
        except:
            return False
