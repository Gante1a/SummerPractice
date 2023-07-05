import json
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from database import DatabaseConnector

class UserTracker:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        self.bot_token = config_data['bot_token']
        self.db_connector = DatabaseConnector()

    def handle_message(self, update: telegram.Update, context):
        # Получение сообщения из обновления
        message = update.message
        chat_id = message.from_user.id
        first_name = message.from_user.first_name
        username = message.from_user.username
        # Проверка наличия chat_id в базе данных
        cursor = self.db_connector.cursor()
        query = "SELECT * FROM users WHERE chat_id = %s"
        values = (chat_id,)
        cursor.execute(query, values)

        if len(cursor.fetchall()) == 0:
            # Добавление данных в базу данных
            insert_query = "INSERT INTO telegramm.users (chat_id, first_name, username) VALUES (%s, %s, %s)"
            insert_values = (chat_id, first_name, username)
            cursor.execute(insert_query, insert_values)
            self.db_connector.commit()
            cursor.close()
            # проверка работоспособности, конечно же в финальной версии будет убрано
            message.reply_text("Спасибо, ваши данные сохранены!")
        else:
            cursor.close()
            message.reply_text("Ваши данные уже сохранены в базе данных!")

        # Запуск самой функции
    def run(self):
        updater = Updater(token=self.bot_token)
        updater.dispatcher.add_handler(MessageHandler(Filters.all, self.handle_message))
        updater.start_polling()
        updater.idle()

# Использование класса
tracker = UserTracker()
tracker.run()