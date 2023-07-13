import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserMain(Base):
    # Данные для таблицы users_main
    __tablename__ = 'users_main'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    __table_args__ = {'schema': schema_name}
    chat_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(1000))
    username = Column(String(1000))

class UserOptional(Base):
    # Данные для таблицы users_optional
    __tablename__ = 'users_optional'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    __table_args__ = {'schema': schema_name}
    chat_id = Column(BigInteger, primary_key=True)
    official_name = Column(String(1000))
    group = Column(String(1000))

class UserMessages(Base):
    # Данные для таблицы messages
    __tablename__ = 'messages'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    __table_args__ = {'schema': schema_name}
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger)
    message = Column(String(1000))
    time = Column(DateTime, nullable=True)  
    is_sent = Column(Boolean) 

class UserKeys(Base):
    # Данные для таблицы keys
    __tablename__ = 'keys'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    __table_args__ = {'schema': schema_name}
    key = Column(Integer, primary_key=True)
    official_name = Column(String(1000))  


class DatabaseManager:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
        # Данные для подключения    
        self.db_host = config_data['db_host']
        self.db_user = config_data['db_user']
        self.db_password = config_data['db_password']
        self.db_database = config_data['db_database']
        self.engine = create_engine(f"mysql+mysqlconnector://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_database}")
        # Создание сессии
        Base.metadata.create_all(bind=self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def close(self):
        self.session.close()
