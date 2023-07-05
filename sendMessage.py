import json
import requests
from jinja2 import Template
from database import DatabaseConnector

class MessageSender:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
        
        self.bot_token = config_data['bot_token']
        self.template = Template(config_data['template_message'])
        self.db_connector = DatabaseConnector()
        self.send_message()

    def send_message(self):
        text_id = input('Введите text_id пользователя: \n')
        message = input('Введите сообщение для отправки: \n')

        sql = f"SELECT chat_id FROM users WHERE chat_id = '{text_id}'"

        connection = self.db_connector.connect()
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        message_text = self.template.render(message=message)

        if len(rows) == 0:
            print('Введённые данные некорректные, повторите ввод')
            self.send_message()
            return

        for row in rows:
            user_chat_id = row[0]
            send_message_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            payload = {
                'chat_id': user_chat_id,
                'text': message_text
            }
            response = requests.post(send_message_url, json=payload)
            if response.status_code == 200:
                print('Сообщение было успешно отправлено пользователю')

        cursor.close()
        connection.close()

sender = MessageSender()
