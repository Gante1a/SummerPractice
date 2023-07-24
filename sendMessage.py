import json
from jinja2 import Template
from datetime import datetime
from database import DatabaseManager, UserMain, UserMessages
import time
import httpx

class MessageSender:
    def __init__(self, chat_id, message):
        self.chat_id = chat_id
        self.message = message

        try:
            # Открытие JSON файла
            with open('config.json', 'r', encoding='utf-8') as file:
                config_data = json.load(file)

            self.bot_token = config_data['bot_token']
            self.template = Template(config_data['template_message'])
            self.database = DatabaseManager(config_file='config.json')

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Ошибка при загрузке конфигурационного файла: {str(e)}")

    async def send_message(self):
        '''отправка сообщения пользователю по chat_id'''
        try:
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

            async def check_internet_connection():
                try:
                    # Проверка подключения к интернету
                    async with httpx.AsyncClient() as client:
                        response = await client.get("https://web.telegram.org")
                        return response.status_code == 200
                except:
                    return False

            while True:
                if await check_internet_connection():
                    # Отправка сообщения
                    send_message_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                    data = {
                        'chat_id': user.chat_id,
                        'text': message_text
                    }
                    async with httpx.AsyncClient() as client:
                        response = await client.post(send_message_url, json=data)
                        if response.status_code == 200:
                            print('Сообщение было успешно отправлено пользователю')
                            # Обновление статуса сообщения в базе данных на 1 (отправлено)
                            new_message.is_sent = True
                            self.database.session.commit()
                        else:
                            print('Внутренняя ошибка при отправке сообщения')
                    break
                else:
                    print('Сообщение не было отправлено, проверьте подключение к интернету')
                    print('Ожидание подключения к интернету...')
                    time.sleep(5)

        except Exception as e:
            raise Exception(f"Ошибка при отправке сообщения: {str(e)}")

        finally:
            self.database.close()
