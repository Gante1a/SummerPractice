import json
import requests
from database import DatabaseConnector

class UserTracker:
    def __init__(self, config_file='config.json'):
        # Загрузка данных конфигурации
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        self.bot_token = config_data['bot_token']
        self.url = f"https://api.telegram.org/bot{self.bot_token}/"

        self.db_connector = DatabaseConnector(config_file)

    def handle_message(self, update):
        # Получение сообщения из обновления
        message = update['message']
        chat_id = message['from']['id']
        first_name = message['from']['first_name']
        username = message['from']['username']

        # Проверка наличия chat_id в базе данных
        if self.check_user_exists(chat_id):
            # Добавление данных в базу
            self.save_user_data(chat_id, first_name, username)
            # проверка работоспособности, конечно же в финальной версии будет убрано
            self.reply_text(chat_id, "Спасибо, ваши данные сохранены!")
        else:
            self.reply_text(chat_id, "Ваши данные уже сохранены в базе данных!")

    def check_user_exists(self, chat_id):
        # Проверка наличия пользователя в базе данных
        cursor = self.db_connector.cursor()
        query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result is None

    def save_user_data(self, chat_id, first_name, username):
        # Сохранение данных пользователя в базе данных
        cursor = self.db_connector.cursor()
        query = f"INSERT INTO telegramm.users (chat_id, first_name, username) VALUES ({chat_id}, '{first_name}', '{username}')"
        cursor.execute(query)
        self.db_connector.commit()
        cursor.close()

    def reply_text(self, chat_id, text):
        # Отправка текстового сообщения пользователю
        reply_url = f"{self.url}sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        response = requests.post(reply_url, json=payload)
        if response.status_code != 200:
            print('Ошибка при отправке сообщения')

    def run(self):
        # Запуск обработки сообщений
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
