import mysql.connector
import json

class DatabaseConnector:
    def __init__(self, config_file='config.json'):
        # Открытие JSON файла
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        # Получение параметров подключения к базе
        self.db_host = config_data['db_host']
        self.db_user = config_data['db_user']
        self.db_password = config_data['db_password']
        self.db_name = config_data['db_database']
        self.connection = None

    # Подключение к базе данных
    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        return self.connection
    
    # Возвращает курсор для операций с бд
    def cursor(self):
        if self.connection is None:
            self.connect()
        return self.connection.cursor()

    # Применяет изменения в бд
    def commit(self):
        if self.connection is not None:
            self.connection.commit()

    # Закрывает соединение с бд
    def close(self):
        if self.connection is not None:
            self.connection.close()

