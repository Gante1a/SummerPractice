import re
from datetime import datetime, timedelta
from jinja2 import Template
import json

class LogReader:
    def __init__(self, config_file='config.json'):
        try:
            # Открытие JSON файла
            with open(config_file, 'r', encoding='utf-8') as file:
                config_data = json.load(file)

            self.template_logs1 = config_data['template_logs1']
            self.template_logs2 = config_data['template_logs2']
            self.target_database = config_data['db_database']
            self.log_file = config_data['log_file']
            self.template1 = Template(self.template_logs1)
            self.template2 = Template(self.template_logs2)

            # Вызов метода read_logs() в конструкторе
            self.read_logs()

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Ошибка при загрузке конфигурационного файла: {str(e)}")

    def read_logs(self):
        try:
            choice = input("Что вывести: (1) пользователей или (2) сообщения? \n")
            if choice == '1':
                self.read_users_logs()
            elif choice == '2':
                self.read_messages_logs()
            else:
                print("Некорректный выбор.")

        except Exception as e:
            raise Exception(f"Ошибка при чтении логов: {str(e)}")

    def read_users_logs(self):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # Выбор значений в скобках после каждого VALUES (определительная черта INSERT)
                pattern = r'(INTO\s+{0}\.users_main.*?)VALUES \((.*?)\).*\n(.*)'.format(self.target_database)
                matches = re.findall(pattern, content, re.MULTILINE)

                for match in matches:
                    values = match[1].replace("'", "").split(", ")
                    date_str = match[2].split(' ', 1)[0].replace('T', ' ').replace('Z', '')
                    # +3 часа для московского часового пояса
                    date = datetime.strptime(date_str.split('.', 1)[0], '%Y-%m-%d %H:%M:%S')
                    updated_date = date + timedelta(hours=3)
                    updated_date_str = updated_date.strftime('%Y-%m-%d %H:%M:%S')

                    # Передача данных в шаблон
                    data = {
                        'chat_id': values[0],
                        'username': values[1],
                        'link': values[2],
                        'date': updated_date_str
                    }

                    output = self.template1.render(data)
                    print(output)

        except Exception as e:
            raise Exception(f"Ошибка при чтении логов пользователей: {str(e)}")

    def read_messages_logs(self):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as file:
                content = file.read()
                # Выбор значений в скобках после каждого VALUES (определительная черта INSERT)
                pattern = r'(INTO\s+{0}\.messages.*?)VALUES \((.*?)\).*\n(.*)'.format(self.target_database)
                matches = re.findall(pattern, content, re.MULTILINE)

                for match in matches:
                    values = match[1].replace("'", "").split(", ")
                    date_str = match[2].split(' ', 1)[0].replace('T', ' ').replace('Z', '')
                    # +3 часа для московского часового пояса
                    date = datetime.strptime(date_str.split('.', 1)[0], '%Y-%m-%d %H:%M:%S')
                    updated_date = date + timedelta(hours=3)
                    updated_date_str = updated_date.strftime('%Y-%m-%d %H:%M:%S')

                    # Передача данных в шаблон
                    data = {
                        'chat_id': values[0],
                        'message': values[1],
                        'date': updated_date_str
                    }

                    output = self.template2.render(data)
                    print(output)

        except Exception as e:
            raise Exception(f"Ошибка при чтении логов сообщений: {str(e)}")

# Использование класса
try:
    reader = LogReader()
except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
