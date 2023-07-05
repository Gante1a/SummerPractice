import json
from telegram import Bot
from jinja2 import Template
from database import DatabaseConnector
import asyncio

class MessageSender:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
        
        self.bot_token = config_data['bot_token']
        self.template = Template(config_data['template_message'])
        self.telegramBot = Bot(token=self.bot_token)
        self.db_connector = DatabaseConnector()

    async def send_message(self):
        # Запрос ввода данных 
        text_id = input('Введите text_id пользователя: ')
        message = input('Введите сообщение для отправки: ')

        # Выбор chat_id по chat_id
        sql = f"SELECT chat_id FROM users WHERE chat_id = '{text_id}'"

        connection = self.db_connector.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        message_text = self.template.render(message=message)

        # Если введённые данные ошибочны, сообщение не отправится
        if len(rows) == 0:
            print('Введённые данные некорректные, повторите ввод')
            await self.send_message()
            return

        # Перебор результатов запроса для отправки сообщения
        for row in rows:
            user_chat_id = row[0]
            self.telegramBot.send_message(chat_id=user_chat_id, text=message_text)

        cursor.close()
        connection.close()
        print('Сообщение было успешно отправлено пользователю')

    # Запуск асинхронной функции
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.send_message())

# Использование класса
sender = MessageSender()
sender.run()
