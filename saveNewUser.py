import json
import requests
from database import DatabaseManager, User

class UserTracker:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        self.bot_token = config_data['bot_token']
        self.url = f"https://api.telegram.org/bot{self.bot_token}/"
        self.database = DatabaseManager(config_file=config_file)

    def handle_message(self, update):
        # Данные для таблицы
        message = update['message']
        chat_id = message['from']['id']
        first_name = message['from']['first_name']
        username = message['from']['username']
        user = self.database.session.query(User).filter_by(chat_id=chat_id).first()
        # Отправка данных
        if user is None:
            self.save_user_data(chat_id, first_name, username)
            self.reply_text(chat_id, "Спасибо, ваши данные сохранены!")
        else:
            self.reply_text(chat_id, "Ваши данные уже сохранены в базе данных!")

    def save_user_data(self, chat_id, first_name, username):
        # Сохранение данных в таблицу
        user = User(chat_id=chat_id, first_name=first_name, username=username)
        self.database.session.add(user)
        self.database.session.commit()

    def reply_text(self, chat_id, text):
        # Отправка сообщения пользователю
        reply_url = f"{self.url}sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(reply_url, json=payload)
        if response.status_code != 200:
            print('Ошибка при отправке сообщения')

    def run(self):
        # Запуск кода
        offset = None
        while True:
            updates_url = f"{self.url}getUpdates?offset={offset}"
            response = requests.get(updates_url)
            json_response = response.json()
            if response.status_code == 200 and json_response['ok']:
                updates = json_response['result']
                if updates:
                    for update in updates:
                        self.handle_message(update)
                        offset = update['update_id'] + 1

# Использование класса
tracker = UserTracker()
tracker.run()
