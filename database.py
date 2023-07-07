import json
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    # Данные для таблицы users
    __tablename__ = 'users'
    with open('config.json', 'r', encoding='utf-8') as file:
        config_data = json.load(file)
        schema_name = config_data['db_database']

    __table_args__ = {'schema': schema_name}
    chat_id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    username = Column(String(255))

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
