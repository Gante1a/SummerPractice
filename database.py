import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.exc

Base = declarative_base()

class UserMain(Base):
    '''Данные для таблицы users_main'''
    __tablename__ = 'users_main'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    try:
        __table_args__ = {'schema': schema_name}
    except KeyError:
        raise Exception("Ошибка: Не удалось получить имя схемы таблицы 'users_main'")
    
    chat_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(1000))
    username = Column(String(1000))

class UserOptional(Base):
    '''Данные для таблицы users_optional'''
    __tablename__ = 'users_optional'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    try:
        __table_args__ = {'schema': schema_name}
    except KeyError:
        raise Exception("Ошибка: Не удалось получить имя схемы таблицы 'users_optional'")
    
    chat_id = Column(BigInteger, primary_key=True)
    official_name = Column(String(1000))
    group = Column(String(1000))

class UserMessages(Base):
    '''Данные для таблицы messages'''
    __tablename__ = 'messages'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    try:
        __table_args__ = {'schema': schema_name}
    except KeyError:
        raise Exception("Ошибка: Не удалось получить имя схемы таблицы 'messages'")
    
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    message = Column(String(1000))
    time = Column(DateTime, nullable=True)  
    is_sent = Column(Boolean) 

class UserKeys(Base):
    '''Данные для таблицы keys'''
    __tablename__ = 'keys'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    try:
        __table_args__ = {'schema': schema_name}
    except KeyError:
        raise Exception("Ошибка: Не удалось получить имя схемы таблицы 'keys'")
    
    key = Column(String(1000), primary_key=True)
    official_name = Column(String(1000))  


class DatabaseManager:
    def __init__(self, config_file='config.json'):
        try:
            with open(config_file, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
        except FileNotFoundError:
            raise Exception(f"Файл конфигурации '{config_file}' не найден.")
        except json.JSONDecodeError as e:
            raise Exception(f"Ошибка при чтении файла '{config_file}': {str(e)}")
        
        self.db_host = config_data['db_host']
        self.db_user = config_data['db_user']
        self.db_password = config_data['db_password']
        self.db_database = config_data['db_database']
        
        try:
            self.engine = create_engine(f"mysql+mysqlconnector://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_database}")
            self.engine.connect()  
        except sqlalchemy.exc.OperationalError as e:
            raise Exception(f"Ошибка подключения к базе данных: {str(e)}")

        try:
            Base.metadata.create_all(bind=self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            raise Exception(f"Ошибка создания сессии базы данных: {str(e)}")

    def close(self):
        self.session.close()
