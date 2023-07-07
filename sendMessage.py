import json
import requests
from jinja2 import Template
from database import DatabaseManager, User

class MessageSender:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
        
        self.bot_token = config_data['bot_token']
        self.template = Template(config_data['template_message'])
        
        self.database = DatabaseManager(config_file=config_file)
        self.send_message()

    def send_message(self):
        # Запрос ввода в консоли
        text_id = input('Введите text_id пользователя: \n')
        message = input('Введите сообщение для отправки: \n')
        # Запрос chat_id по chat_id
        user = self.database.session.query(User).filter_by(chat_id=text_id).first()
        if user is None:
            print('Введённые данные некорректные, повторите ввод')
            self.send_message()
            return
        
        # Применение jinja
        message_text = self.template.render(message=message)
        # Отправка сообщения
        send_message_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': user.chat_id,
            'text': message_text
        }
        response = requests.post(send_message_url, json=payload)
        if response.status_code == 200:
            print('Сообщение было успешно отправлено пользователю')

        self.database.close()

# Использование класса
sender = MessageSender()
