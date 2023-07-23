from database import DatabaseManager, UserMain, UserOptional, UserKeys, UserMessages
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, IntegrityError

def getUsersInfo():
    '''Вывод информации о пользователях'''
    try:
        db_manager = DatabaseManager()
        session = db_manager.session
        result = []

        try:
            user_main_data = session.query(UserMain.chat_id, UserMain.first_name, UserMain.username).all()
            user_optional_data = session.query(UserOptional.chat_id, UserOptional.official_name).all()

            for user_main_row in user_main_data:
                chat_id = user_main_row.chat_id
                first_name = user_main_row.first_name
                username = user_main_row.username
                official_name = ""

                for user_optional_row in user_optional_data:
                    if user_optional_row.chat_id == chat_id:
                        official_name = user_optional_row.official_name or ""
                        break

                result.append((chat_id, first_name, username, official_name))

            return result

        finally:
            db_manager.close()
    except SQLAlchemyError as e:
        raise Exception(f"Ошибка базы данных: {str(e)}")


def insert_key(key: str, official_name: str):
    '''Вставка новых значений в таблицу keys'''
    try:
        db_manager = DatabaseManager()
        session = db_manager.session
        new_key = UserKeys(key=key, official_name=official_name)
        session.add(new_key)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise Exception("Ошибка базы данных при добавлении ключа: Ключ уже существует. Пожалуйста, измените его название.")
    except SQLAlchemyError as e:
        session.rollback()
        raise Exception(f"Ошибка базы данных при добавлении ключа: {str(e)}")
    finally:
        db_manager.close()

def delete_user(chat_id):
    '''Удаление пользователя из таблиц users_main и users_optional по chat_id'''
    try:
        db_manager = DatabaseManager()
        session = db_manager.session
        try:
            user_main_data = session.query(UserMain).filter(UserMain.chat_id == chat_id).one()
            user_optional_data = session.query(UserOptional).filter(UserOptional.chat_id == chat_id).one()

            session.delete(user_main_data)
            session.delete(user_optional_data)
            session.commit()
        except NoResultFound:
            pass
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка базы данных при удалении пользователя: {str(e)}")
    finally:
        db_manager.close()

def getKeysInfo():
    '''Получение ключей из таблицы'''
    try:
        db_manager = DatabaseManager()
        session = db_manager.session
        result = []

        try:
            keys_data = session.query(UserKeys.key, UserKeys.official_name).all()

            for key_row in keys_data:
                key = key_row.key
                official_name = key_row.official_name or ""
                result.append((key, official_name))

            return result

        finally:
            db_manager.close()
    except SQLAlchemyError as e:
        raise Exception(f"Ошибка базы данных: {str(e)}")  

def delete_key(key):
    '''Удаление ключей из таблицы'''
    try:
        db_manager = DatabaseManager()
        session = db_manager.session
        try:
            key_data = session.query(UserKeys).filter(UserKeys.key == key).one()
            session.delete(key_data)
            session.commit()
        except NoResultFound:
            pass
        except Exception as e:
            session.rollback()
            raise Exception(f"Ошибка базы данных при удалении ключа: {str(e)}")
    finally:
        db_manager.close()      

def getMessagesInfo():
    '''Получение всех сообщений из таблицы messages'''
    try:
        db_manager = DatabaseManager()
        session = db_manager.session
        messages_data = session.query(UserMessages).all()
        return messages_data
    except Exception as e:
        raise Exception(f"Ошибка базы данных: {str(e)}")         