import re
from datetime import datetime, timedelta
from jinja2 import Template
import json

class LogReader:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        self.template_logs = config_data['template_logs']
        self.target_database = config_data['db_database']
        self.log_file = config_data['log_file']
        self.template = Template(self.template_logs)

    def read_logs(self):
        with open(self.log_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # Выбор значений в скобках после каждого VALUES (определительная черта INSERT)
            pattern = r'(INTO\s+{0}\.users.*?)VALUES \((.*?)\).*\n(.*)'.format(self.target_database)
            matches = re.findall(pattern, content, re.MULTILINE)

            for match in matches:
                line = match[0]
                values = match[1].replace("'", "").split(", ")
                date_str = match[2].split(' ', 1)[0].replace('T', ' ').replace('Z', '')
                # +3 часа для московского часового пояса
                date = datetime.strptime(date_str.split('.', 1)[0], '%Y-%m-%d %H:%M:%S')
                updated_date = date + timedelta(hours=3)
                updated_date_str = updated_date.strftime('%Y-%m-%d %H:%M:%S')

                # Передача данных в шаблон
                context = {
                    'chat_id': values[0],
                    'username': values[1],
                    'link': values[2],
                    'date': updated_date_str
                }

                output = self.template.render(context)
                print(output)

# Использование класса
reader = LogReader()
reader.read_logs()
